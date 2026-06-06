import anthropic
from config import (
    ANTHROPIC_API_KEY, NICHE, BRAND_NAME, WEBSITE_URL,
    TARGET_AUDIENCE, BRAND_VOICE, YOUTUBE_CHANNEL_URL
)

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

PLATFORM_INSTRUCTIONS = {
    "youtube_longform": {
        "name": "YouTube (Long-Form)",
        "prompt": """Create a complete YouTube video package for this topic:

VIDEO TITLE (40-60 characters, use numbers/power words):
[Write the title here]

VIDEO DESCRIPTION (SEO-optimized, 250-300 words):
[First 2-3 lines hook the viewer — this shows before 'Show more']
[Value the video delivers]
[3-5 key timestamps if applicable]
[CTA: subscribe, visit website, comment]
[10-15 relevant keywords naturally woven in]

VIDEO SCRIPT OUTLINE:
🎯 HOOK (0-30s): [Grab attention with a bold statement, question, or surprising stat]
📖 INTRO (30s-2min): [Establish why this matters, preview what they'll learn]
💡 MAIN VALUE (2-12min): [3-5 key points, each with an example or story]
🎬 OUTRO (last 30s): [Subscribe CTA, tease next video, ask for a comment]

TAGS (12 relevant tags):
[tag1, tag2, tag3, ...]"""
    },
    "youtube_shorts": {
        "name": "YouTube Shorts",
        "prompt": """Create a complete YouTube Shorts package (under 60 seconds):

SHORT TITLE (punchy, under 40 characters):
[Write the title]

SCRIPT:
[0-3s] HOOK: [Say something bold, counterintuitive, or urgent]
[3-15s] SETUP: [Relate to the audience's pain or desire]
[15-45s] VALUE: [The tip, insight, or story — move fast, cut filler]
[45-60s] CTA: [Follow for more / comment your answer below]

CAPTION:
[2-3 punchy sentences]
#Shorts #[niche hashtag] #[broad hashtag]"""
    },
    "tiktok": {
        "name": "TikTok",
        "prompt": """Create a complete TikTok package:

HOOK (first 3 seconds — make it impossible to scroll past):
[The exact opening line or on-screen text]

SCRIPT (30-60 seconds, fast-paced and conversational):
[0-3s] HOOK: [Bold statement, question, or shocking fact]
[3-15s] RELATE: ["I used to..." / "Most people..." / "Here's what nobody tells you..."]
[15-50s] VALUE BOMB: [The actual insight, tip, or story — keep energy high]
[50-60s] CTA: [Follow for more / Comment 'X' if this hit / Share with someone who needs this]

CAPTION (under 150 characters):
[Punchy, drives curiosity]

HASHTAGS (6-8 tags):
#BusinessTips #Entrepreneur #[niche] #[trending concept]

SOUND SUGGESTION:
[Type of audio that fits — trending sound / original audio / voiceover only]"""
    },
    "instagram": {
        "name": "Instagram",
        "prompt": """Create a complete Instagram post package:

CAPTION:
[HOOK — First line only. This is what shows before 'more'. Make it impossible to ignore.]

[Blank line]

[2-3 paragraphs of story, insight, or value. Personal, relatable, punchy.]

[Blank line]

[CTA — Ask a specific question or direct them to act]

. . .

[20-25 hashtags — mix of niche (10k-100k posts) and broad (1M+)]

CONTENT FORMAT SUGGESTION:
[ ] Single image  [ ] Carousel (multi-slide)  [ ] Reel

If carousel, slide structure:
Slide 1: [Hook headline]
Slides 2-8: [One key point per slide]
Slide 9: [CTA / follow]

VISUAL DIRECTION:
[What the image or first slide should look like]"""
    },
    "twitter": {
        "name": "X (Twitter)",
        "prompt": """Create an X (Twitter) thread and a standalone tweet:

THREAD:

1/ [Hook tweet — bold, counterintuitive, or a strong take. Under 280 chars. Makes people need to read on.]

2/ [Expand with context or a personal story]

3/ [Key insight #1 with a concrete example]

4/ [Key insight #2]

5/ [Key insight #3]

6/ [Surprising fact, stat, or reframe]

7/ [What to do with this — practical next step]

8/ [Close with a summary + CTA. "Follow @handle for more. Repost if this was useful."]

---
STANDALONE TWEET (use this if a thread feels like too much):
[Single punchy tweet under 280 chars]"""
    },
    "linkedin": {
        "name": "LinkedIn",
        "prompt": """Create a LinkedIn post:

[Opening line — bold, specific, no "I'm excited to share" openers. Something that stops the feed scroll.]

[Blank line]

[Story or observation — 2-3 short paragraphs, each 1-3 sentences]
[Use lots of white space. Short sentences. Easy to skim.]

[Blank line]

[The real takeaway — what they should walk away knowing or feeling]

[Blank line]

[A specific question to drive comments — not "thoughts?" but something concrete like "Which of these do you struggle with most?"]

#[hashtag1] #[hashtag2] #[hashtag3]

Note: Target 150-300 words. LinkedIn rewards posts people stop and read fully."""
    },
    "facebook": {
        "name": "Facebook",
        "prompt": """Create a Facebook post:

[Opening — conversational, like a real person talking. No corporate speak.]

[Share a story, insight, or behind-the-scenes moment that adds real value]

[If this connects to a YouTube video, tease the video without giving everything away]

[End with a question that drives comments — Facebook's algorithm loves early comment activity]

LINK TO YOUTUBE (if applicable):
[Add video link here]

Keep it under 200 words for best organic reach. 2-3 hashtags max."""
    }
}


def generate_content_for_all_platforms(topic: str, used_topics: list) -> dict:
    used_str = "\n".join(f"- {t}" for t in used_topics[-10:]) if used_topics else "None yet"

    base_context = f"""You are a world-class social media content creator.

BRAND: {BRAND_NAME}
WEBSITE: {WEBSITE_URL}
YOUTUBE: {YOUTUBE_CHANNEL_URL}
NICHE: {NICHE}
TARGET AUDIENCE: {TARGET_AUDIENCE}
BRAND VOICE: {BRAND_VOICE}
TODAY'S TOPIC: {topic}

RECENTLY COVERED (do not repeat these exact angles):
{used_str}

Rules:
- Provide genuine value, not fluff
- Make content feel native to each platform
- Write hooks that stop the scroll
- Include clear calls-to-action
- Everything must be ready to post with no placeholders
- Do not add meta-commentary or explanations — output the content only

"""

    results = {}
    for platform_key, data in PLATFORM_INSTRUCTIONS.items():
        prompt = base_context + f"=== {data['name'].upper()} ===\n\n" + data["prompt"]
        message = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            messages=[{"role": "user", "content": prompt}]
        )
        results[platform_key] = {
            "platform_name": data["name"],
            "content": message.content[0].text
        }

    return results


def generate_topic_ideas(used_topics: list) -> list:
    used_str = "\n".join(f"- {t}" for t in used_topics) if used_topics else "None"

    prompt = f"""You are a content strategist for a {NICHE} creator targeting {TARGET_AUDIENCE}.

Generate 7 fresh, high-engagement content topic ideas.

RECENTLY COVERED (do NOT repeat or closely overlap):
{used_str}

Each topic must be:
- Specific and concrete (never vague)
- Emotionally charged: curiosity, aspiration, urgency, or inspiration
- Works across YouTube, TikTok, Instagram, LinkedIn, and X
- Relevant to {NICHE} in 2025
- Actionable or insightful

Return ONLY a numbered list. No explanations.
Example:
1. Why most entrepreneurs fail in year one (and the 3 decisions that change everything)
2. The $10/day habit that tripled my output
"""

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=500,
        messages=[{"role": "user", "content": prompt}]
    )

    topics = []
    for line in message.content[0].text.strip().split("\n"):
        line = line.strip()
        if line and line[0].isdigit():
            if ". " in line[:4]:
                topic = line.split(". ", 1)[1]
            elif ") " in line[:4]:
                topic = line.split(") ", 1)[1]
            else:
                topic = line
            topics.append(topic.strip())

    return topics[:7]
