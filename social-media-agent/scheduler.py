import asyncio
import logging
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
from config import DAILY_GENERATE_TIME, POSTING_TIMEZONE, TELEGRAM_CHAT_ID
from constants import PLATFORM_EMOJIS
import database as db
import content_generator as cg

logger = logging.getLogger(__name__)


async def daily_content_job(bot):
    logger.info("Running daily content generation...")
    try:
        used = db.get_used_topics(limit=30)
        topics = cg.generate_topic_ideas(used)
        if not topics:
            await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text="⚠️ Daily job: failed to generate topics.")
            return

        topic = topics[0]
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"🌅 *Good morning! Daily content incoming.*\n\nTopic: *{topic}*\n\nGenerating for all 7 platforms...",
            parse_mode="Markdown"
        )

        content_map = cg.generate_content_for_all_platforms(topic, used)
        db.mark_topic_used(topic)

        from telegram import InlineKeyboardButton, InlineKeyboardMarkup

        for platform_key, data in content_map.items():
            post_id = db.save_post(
                platform=platform_key,
                content=data["content"],
                topic=topic,
                status="pending"
            )
            emoji = PLATFORM_EMOJIS.get(platform_key, "📱")
            header = f"{emoji} *{data['platform_name']}*\n{'─' * 28}\n\n"
            preview = data["content"][:3800]

            keyboard = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Approve & Post", callback_data=f"approve_{post_id}"),
                    InlineKeyboardButton("✏️ Edit", callback_data=f"edit_{post_id}"),
                ],
                [
                    InlineKeyboardButton("🔄 Regenerate", callback_data=f"regen_{post_id}"),
                    InlineKeyboardButton("❌ Skip", callback_data=f"skip_{post_id}"),
                ]
            ])

            msg = await bot.send_message(
                chat_id=TELEGRAM_CHAT_ID,
                text=header + preview,
                parse_mode="Markdown",
                reply_markup=keyboard
            )
            db.update_post_status(post_id, "pending", telegram_message_id=msg.message_id)
            await asyncio.sleep(0.4)

        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=f"✅ *{len(content_map)} drafts ready for review!*",
            parse_mode="Markdown"
        )

    except Exception as e:
        logger.error(f"Daily job error: {e}")
        await bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=f"⚠️ Daily job failed: {e}")


def setup_scheduler(bot) -> AsyncIOScheduler:
    tz = pytz.timezone(POSTING_TIMEZONE)
    scheduler = AsyncIOScheduler(timezone=tz)
    hour, minute = DAILY_GENERATE_TIME.split(":")
    scheduler.add_job(
        daily_content_job,
        trigger=CronTrigger(hour=int(hour), minute=int(minute), timezone=tz),
        args=[bot],
        id="daily_content",
        replace_existing=True
    )
    return scheduler
