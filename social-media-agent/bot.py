import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    MessageHandler, filters, ContextTypes
)
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from constants import PLATFORM_EMOJIS, SCRIPT_ONLY_NOTES
import database as db
import content_generator as cg
from platforms import get_publisher

logger = logging.getLogger(__name__)


def _keyboard(post_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("✅ Approve & Post", callback_data=f"approve_{post_id}"),
            InlineKeyboardButton("✏️ Edit", callback_data=f"edit_{post_id}"),
        ],
        [
            InlineKeyboardButton("🔄 Regenerate", callback_data=f"regen_{post_id}"),
            InlineKeyboardButton("❌ Skip", callback_data=f"skip_{post_id}"),
        ]
    ])


def _preview(content: str) -> str:
    return content[:3800] + "\n\n_[...truncated for preview]_" if len(content) > 3800 else content


async def send_platform_drafts(chat_id, bot, topic: str, content_map: dict):
    """Send all generated drafts to the user for review."""
    for platform_key, data in content_map.items():
        post_id = db.save_post(
            platform=platform_key,
            content=data["content"],
            topic=topic,
            status="pending"
        )
        emoji = PLATFORM_EMOJIS.get(platform_key, "📱")
        header = f"{emoji} *{data['platform_name']}*\n{'─' * 28}\n\n"
        msg = await bot.send_message(
            chat_id=chat_id,
            text=header + _preview(data["content"]),
            parse_mode="Markdown",
            reply_markup=_keyboard(post_id)
        )
        db.update_post_status(post_id, "pending", telegram_message_id=msg.message_id)
        await asyncio.sleep(0.4)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 *Social Media Agent is live!*\n\n"
        "I generate content for all your platforms and send it here for approval.\n\n"
        "*Commands:*\n"
        "/generate — Auto-generate today's content\n"
        "/topic <your idea> — Generate content on a specific topic\n"
        "/pending — View posts waiting for approval\n"
        "/recent — See recent post history\n"
        "/help — Show this message",
        parse_mode="Markdown"
    )


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🤖 *Commands*\n\n"
        "*/generate* — Pick a topic automatically and create content\n"
        "*/topic [idea]* — Create content around your own topic\n"
        "*/pending* — See posts awaiting approval\n"
        "*/recent* — See what's been posted\n\n"
        "*Reviewing drafts:*\n"
        "✅ Approve & Post — publish immediately\n"
        "✏️ Edit — rewrite then approve\n"
        "🔄 Regenerate — get a fresh version\n"
        "❌ Skip — discard this draft",
        parse_mode="Markdown"
    )


async def generate_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        return
    status = await update.message.reply_text("🧠 Picking today's topic...")
    try:
        used = db.get_used_topics(limit=30)
        topics = cg.generate_topic_ideas(used)
        if not topics:
            await status.edit_text("❌ Couldn't generate topics. Check your ANTHROPIC_API_KEY.")
            return
        topic = topics[0]
        await status.edit_text(
            f"✍️ Creating content for:\n\n*{topic}*\n\nGenerating for all 7 platforms...",
            parse_mode="Markdown"
        )
        content_map = cg.generate_content_for_all_platforms(topic, used)
        db.mark_topic_used(topic)
        await status.edit_text(
            f"✅ *Content ready!*\n\nTopic: _{topic}_\n\nSending drafts...",
            parse_mode="Markdown"
        )
        await send_platform_drafts(update.effective_chat.id, context.bot, topic, content_map)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📋 *{len(content_map)} drafts sent for review.* Approve, edit, or skip each one.",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"generate_cmd error: {e}")
        await status.edit_text(f"❌ Error: {e}")


async def topic_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        return
    topic = " ".join(context.args).strip() if context.args else ""
    if not topic:
        await update.message.reply_text(
            "Please add a topic:\n`/topic Your topic here`",
            parse_mode="Markdown"
        )
        return
    status = await update.message.reply_text(
        f"✍️ Creating content for:\n\n*{topic}*\n\nGenerating for all 7 platforms...",
        parse_mode="Markdown"
    )
    try:
        used = db.get_used_topics()
        content_map = cg.generate_content_for_all_platforms(topic, used)
        db.mark_topic_used(topic)
        await status.edit_text(
            f"✅ *Content ready!* Sending drafts...",
            parse_mode="Markdown"
        )
        await send_platform_drafts(update.effective_chat.id, context.bot, topic, content_map)
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=f"📋 *{len(content_map)} drafts sent for review.*",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"topic_cmd error: {e}")
        await status.edit_text(f"❌ Error: {e}")


async def pending_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        return
    pending = db.get_pending_posts()
    if not pending:
        await update.message.reply_text("✅ No pending posts. Use /generate to create content.")
        return
    lines = [f"📋 *{len(pending)} pending posts:*\n"]
    for p in pending[:10]:
        emoji = PLATFORM_EMOJIS.get(p["platform"], "📱")
        lines.append(f"{emoji} {p['platform']} — _{p['topic'][:60] if p['topic'] else 'no topic'}_")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def recent_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if str(update.effective_chat.id) != TELEGRAM_CHAT_ID:
        return
    posts = db.get_recent_posts(limit=10)
    if not posts:
        await update.message.reply_text("No posts yet. Run /generate to get started!")
        return
    icons = {"posted": "✅", "pending": "⏳", "skipped": "❌", "failed": "⚠️",
             "script_ready": "📋", "approved": "✅"}
    lines = ["*📊 Recent Posts:*\n"]
    for p in posts:
        emoji = PLATFORM_EMOJIS.get(p["platform"], "📱")
        icon = icons.get(p["status"], "❓")
        date = p["created_at"][:10] if p["created_at"] else ""
        lines.append(f"{icon} {emoji} {p['platform']} — {date}")
        if p["topic"]:
            lines.append(f"   _{p['topic'][:55]}_")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    action, post_id_str = query.data.split("_", 1)
    post_id = int(post_id_str)
    post = db.get_post(post_id)

    if not post:
        await query.edit_message_reply_markup(reply_markup=None)
        return

    if action == "skip":
        db.update_post_status(post_id, "skipped")
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(f"❌ Skipped {PLATFORM_EMOJIS.get(post['platform'], '')} {post['platform']} post.")

    elif action == "edit":
        context.user_data["editing_post_id"] = post_id
        await query.edit_message_reply_markup(reply_markup=None)
        await query.message.reply_text(
            "✏️ *Edit mode*\n\nSend the new content for this post. Or /cancel to keep the original.",
            parse_mode="Markdown"
        )

    elif action == "approve":
        await query.edit_message_reply_markup(reply_markup=None)
        platform = post["platform"]
        publisher = get_publisher(platform)

        if publisher is None:
            # Script-only platform
            db.update_post_status(post_id, "script_ready")
            note = SCRIPT_ONLY_NOTES.get(platform, "📋 Script approved and saved.")
            await query.message.reply_text(note, parse_mode="Markdown")
            return

        status_msg = await query.message.reply_text(f"⏳ Posting to {platform}...")
        try:
            result = publisher.post(post["content"])
            if result.get("success"):
                db.update_post_status(
                    post_id, "posted",
                    post_url=result.get("url"),
                    posted_time=result.get("posted_time")
                )
                await status_msg.edit_text(
                    f"✅ Posted to *{platform}*!\n{result.get('url', '')}",
                    parse_mode="Markdown"
                )
            else:
                db.update_post_status(post_id, "failed")
                err = result.get("error", "Unknown error")
                await status_msg.edit_text(
                    f"⚠️ Could not post to {platform}:\n_{err}_\n\nContent saved — check your API credentials in .env.",
                    parse_mode="Markdown"
                )
        except Exception as e:
            db.update_post_status(post_id, "failed")
            await status_msg.edit_text(f"❌ Error: {e}")

    elif action == "regen":
        await query.edit_message_text(
            query.message.text + "\n\n_🔄 Regenerating..._",
            parse_mode="Markdown"
        )
        try:
            used = db.get_used_topics()
            new_map = cg.generate_content_for_all_platforms(post["topic"], used)
            if post["platform"] in new_map:
                new_content = new_map[post["platform"]]["content"]
                db.update_post_content(post_id, new_content)
                platform_name = new_map[post["platform"]]["platform_name"]
                emoji = PLATFORM_EMOJIS.get(post["platform"], "📱")
                header = f"{emoji} *{platform_name}* _(regenerated)_\n{'─' * 28}\n\n"
                await query.edit_message_text(
                    header + _preview(new_content),
                    parse_mode="Markdown",
                    reply_markup=_keyboard(post_id)
                )
        except Exception as e:
            await query.message.reply_text(f"❌ Regeneration failed: {e}")


async def handle_edit_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    post_id = context.user_data.get("editing_post_id")
    if not post_id:
        return
    new_content = update.message.text
    db.update_post_content(post_id, new_content)
    db.update_post_status(post_id, "pending")
    post = db.get_post(post_id)
    context.user_data.pop("editing_post_id", None)
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("✅ Approve & Post", callback_data=f"approve_{post_id}"),
        InlineKeyboardButton("❌ Skip", callback_data=f"skip_{post_id}"),
    ]])
    await update.message.reply_text(
        f"✅ Content updated for *{post['platform']}*. Ready to post?",
        parse_mode="Markdown",
        reply_markup=keyboard
    )


async def cancel_edit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.pop("editing_post_id", None)
    await update.message.reply_text("Edit cancelled.")


def build_application() -> Application:
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("generate", generate_cmd))
    app.add_handler(CommandHandler("topic", topic_cmd))
    app.add_handler(CommandHandler("pending", pending_cmd))
    app.add_handler(CommandHandler("recent", recent_cmd))
    app.add_handler(CommandHandler("cancel", cancel_edit))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_edit_text))
    return app
