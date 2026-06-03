import os
from dotenv import load_dotenv

load_dotenv()

# Claude AI
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

# Telegram
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")

# Twitter/X
TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN", "")
TWITTER_ACCESS_TOKEN_SECRET = os.getenv("TWITTER_ACCESS_TOKEN_SECRET", "")
TWITTER_BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN", "")

# Instagram / Facebook (via Meta Graph API)
INSTAGRAM_ACCESS_TOKEN = os.getenv("INSTAGRAM_ACCESS_TOKEN", "")
INSTAGRAM_ACCOUNT_ID = os.getenv("INSTAGRAM_ACCOUNT_ID", "")
FACEBOOK_ACCESS_TOKEN = os.getenv("FACEBOOK_ACCESS_TOKEN", "")
FACEBOOK_PAGE_ID = os.getenv("FACEBOOK_PAGE_ID", "")

# LinkedIn
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_PERSON_URN = os.getenv("LINKEDIN_PERSON_URN", "")

# Brand settings
NICHE = os.getenv("NICHE", "Business / Entrepreneurship")
BRAND_NAME = os.getenv("BRAND_NAME", "My Brand")
WEBSITE_URL = os.getenv("WEBSITE_URL", "")
YOUTUBE_CHANNEL_URL = os.getenv("YOUTUBE_CHANNEL_URL", "")
TARGET_AUDIENCE = os.getenv("TARGET_AUDIENCE", "entrepreneurs, business owners, and aspiring professionals")
BRAND_VOICE = os.getenv("BRAND_VOICE", "authentic, direct, and value-driven")

# Scheduling
DAILY_GENERATE_TIME = os.getenv("DAILY_GENERATE_TIME", "08:00")
POSTING_TIMEZONE = os.getenv("POSTING_TIMEZONE", "America/New_York")

# Database
DATABASE_PATH = os.getenv("DATABASE_PATH", "social_media_agent.db")
