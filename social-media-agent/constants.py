PLATFORM_EMOJIS = {
    "youtube_longform": "📺",
    "youtube_shorts": "🎬",
    "tiktok": "🎵",
    "instagram": "📸",
    "twitter": "🐦",
    "linkedin": "💼",
    "facebook": "👥",
}

PLATFORM_NAMES = {
    "youtube_longform": "YouTube (Long-Form)",
    "youtube_shorts": "YouTube Shorts",
    "tiktok": "TikTok",
    "instagram": "Instagram",
    "twitter": "X (Twitter)",
    "linkedin": "LinkedIn",
    "facebook": "Facebook",
}

SCRIPT_ONLY_PLATFORMS = {"youtube_longform", "youtube_shorts", "tiktok"}

SCRIPT_ONLY_NOTES = {
    "youtube_longform": (
        "📋 *YouTube Long-Form Script Approved*\n\n"
        "Your script, title, and description are saved.\n"
        "Record your video using this script, then upload to YouTube Studio "
        "and paste the generated title/description."
    ),
    "youtube_shorts": (
        "📋 *YouTube Shorts Script Approved*\n\n"
        "Script saved. Record a vertical video (under 60 seconds) "
        "and upload it as a YouTube Short."
    ),
    "tiktok": (
        "📋 *TikTok Script Approved*\n\n"
        "Script saved. Record your video using this script, "
        "then post manually via the TikTok app or schedule through Buffer/Later."
    ),
}
