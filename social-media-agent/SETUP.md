# Social Media Agent — Setup Guide

This guide walks you through setting up your automated social media agent step by step. No coding experience required.

---

## What This Agent Does

- **Every morning** (at the time you set), it generates content for all 7 platforms
- **Sends drafts to your Telegram** so you can review before anything goes live
- You **Approve, Edit, Regenerate, or Skip** each post with one tap
- **Approved posts publish instantly** to Twitter/X, LinkedIn, and Facebook
- For **YouTube and TikTok**, it generates ready-to-use scripts — you record and upload
- For **Instagram**, it generates the caption — you pair it with an image

---

## Prerequisites

You need the following installed on your computer:

- **Python 3.11 or newer** — [Download here](https://python.org/downloads)
- A terminal / command prompt

Check your Python version by opening a terminal and typing:
```
python --version
```

---

## Step 1 — Download and Install

```bash
# Go into the agent folder
cd social-media-agent

# Install all required packages
pip install -r requirements.txt
```

---

## Step 2 — Create Your Configuration File

```bash
cp .env.example .env
```

Open the `.env` file in any text editor (Notepad on Windows, TextEdit on Mac) and fill in your values. The sections below explain where to get each key.

---

## Step 3 — Get Your API Keys

### 3A — Claude AI (Required)

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Click **API Keys** in the left sidebar
4. Click **Create Key**, name it "Social Media Agent"
5. Copy the key (starts with `sk-ant-`) and paste it into `.env`:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

---

### 3B — Telegram Bot (Required — this is how you control the agent)

**Create your bot:**
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts — give your bot a name and username
4. BotFather gives you a token like `123456789:ABCdef...`
5. Paste it into `.env`:
   ```
   TELEGRAM_BOT_TOKEN=123456789:ABCdef...
   ```

**Find your Chat ID:**
1. Search for **@userinfobot** on Telegram
2. Send it any message
3. It replies with your user ID — a number like `987654321`
4. Paste it into `.env`:
   ```
   TELEGRAM_CHAT_ID=987654321
   ```

---

### 3C — Twitter / X (Optional — enables auto-posting)

1. Go to [developer.twitter.com](https://developer.twitter.com)
2. Sign in with your Twitter/X account
3. Click **+ Create Project**, then create an App inside it
4. Under your App → **Keys and Tokens**: copy Bearer Token, API Key, API Key Secret
5. Under "Access Token and Secret" click **Generate** → copy both values
6. Set App permissions to **Read and Write**
7. Paste all 5 values into `.env`

---

### 3D — Facebook Page (Optional — enables auto-posting)

Requires a Facebook Business Page (not personal profile).

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps** → **Create App** → choose **Business**
3. Add the **Facebook Login** product
4. Go to **Tools** → **Graph API Explorer**
5. Select your App, generate a token with permissions: `pages_manage_posts`, `pages_read_engagement`
6. Switch to **Page Token** and select your Page
7. Copy the token + your Page ID (found on your Page under About)
8. Paste into `.env`:
   ```
   FACEBOOK_ACCESS_TOKEN=your_long_token
   FACEBOOK_PAGE_ID=123456789
   ```

> **Note:** For a permanent token, follow the [long-lived token guide](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived).

---

### 3E — Instagram (Optional — generates captions for manual posting)

Requires an Instagram Professional account linked to your Facebook Page.

1. In your Facebook Developer App (from 3D), go to **Graph API Explorer**
2. Generate a **User Access Token** with: `instagram_basic`, `instagram_content_publish`
3. To find your Instagram Account ID, call: `GET /me/accounts` then `GET /{page-id}?fields=instagram_business_account`
4. Paste into `.env`:
   ```
   INSTAGRAM_ACCESS_TOKEN=your_token
   INSTAGRAM_ACCOUNT_ID=your_instagram_id
   ```

> **Note:** Instagram requires an image for feed posts. The agent generates the caption — you pair it with a photo.

---

### 3F — LinkedIn (Optional — enables auto-posting)

1. Go to [developer.linkedin.com](https://developer.linkedin.com)
2. Click **Create App**
3. Under **Products**, request **Share on LinkedIn** and **Sign In with LinkedIn**
4. Go to **Auth** → OAuth 2.0 tools → generate an access token with scope: `w_member_social`
5. Get your Person URN by calling: `https://api.linkedin.com/v2/me` with the token
   — your URN is `urn:li:person:YOUR_ID`
6. Paste into `.env`:
   ```
   LINKEDIN_ACCESS_TOKEN=your_token
   LINKEDIN_PERSON_URN=urn:li:person:XXXXXXXX
   ```

> **Note:** LinkedIn tokens expire after 60 days. Set a reminder to refresh.

---

### 3G — TikTok and YouTube (No API key needed)

The agent **automatically generates complete scripts** for both platforms.

- **TikTok**: Record your video using the script, post via TikTok app or [Buffer](https://buffer.com)
- **YouTube Long-Form**: Record using the script. Paste the generated title/description when uploading.
- **YouTube Shorts**: Record vertical video under 60 seconds. Upload as a Short.

---

## Step 4 — Fill In Your Brand Info

In `.env`, update the brand section to match your actual brand:

```
NICHE=Business / Entrepreneurship
BRAND_NAME=Your Actual Name or Brand
WEBSITE_URL=https://yourwebsite.com
YOUTUBE_CHANNEL_URL=https://youtube.com/@yourchannel
TARGET_AUDIENCE=entrepreneurs and ambitious professionals aged 25-45
BRAND_VOICE=direct, authentic, no fluff — like a mentor talking to a friend
DAILY_GENERATE_TIME=08:00
POSTING_TIMEZONE=America/New_York
```

The more specific your audience and voice, the better the content.

**Common timezones:** `America/Los_Angeles` · `America/Chicago` · `America/New_York` · `Europe/London` · `Asia/Dubai` · `Asia/Singapore`

---

## Step 5 — Start the Agent

```bash
python main.py
```

You should see:
```
[INFO] Database ready.
[INFO] Scheduler started.
[INFO] Bot running. Open Telegram and send /generate to create content now.
```

Open Telegram, find your bot, and send `/start` then `/generate`.

---

## Daily Usage

| Command | What it does |
|---|---|
| `/generate` | Auto-pick a topic and generate content for all platforms |
| `/topic 5 lessons from my first failed startup` | Generate content for your specific topic |
| `/pending` | See posts waiting for your approval |
| `/recent` | See what's been posted recently |

**When reviewing a draft:**
- **✅ Approve & Post** — publishes immediately
- **✏️ Edit** — type your revision, then confirm
- **🔄 Regenerate** — Claude writes a completely new version
- **❌ Skip** — discards the draft

---

## Running 24/7

**Option A — Mac/Linux background process:**
```bash
nohup python main.py &
```

**Option B — Deploy to [Railway](https://railway.app) (recommended, free tier available):**
1. Push the `social-media-agent` folder to a GitHub repo
2. Connect Railway to that repo
3. Add all `.env` values in Railway's environment variables tab
4. Deploy — it runs 24/7 automatically

**Option C:** Any VPS (DigitalOcean, Hetzner) using `screen` or `systemd`.

---

## Troubleshooting

**Bot doesn't respond:** Check `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` in `.env`. Make sure the agent is running.

**Content generation fails:** Check `ANTHROPIC_API_KEY` is valid and has credits.

**Twitter posting fails:** Your Twitter app needs **Read and Write** permissions. Regenerate access tokens after changing permissions.

**LinkedIn token expired:** LinkedIn tokens last 60 days. Repeat Step 3F.

**Facebook token expired:** Create a long-lived token (Step 3D note).

---

## Platform Summary

| Platform | What the agent does |
|---|---|
| Twitter/X | Writes + posts full threads automatically |
| LinkedIn | Writes + posts professional content |
| Facebook | Writes + posts to your Page |
| Instagram | Writes the caption — you add an image |
| TikTok | Writes the script — you record and post |
| YouTube Long-Form | Writes title, description, full script — you record and upload |
| YouTube Shorts | Writes the short script — you record and upload |
