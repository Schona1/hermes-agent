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

You need the following installed on your computer or server:

- **Python 3.11 or newer** — [Download here](https://python.org/downloads)
- A terminal / command prompt

Check your Python version by opening a terminal and typing:
```
python --version
```

---

## Step 1 — Download and Install

```bash
# 1. Go into the agent folder
cd social-media-agent

# 2. Install all required packages
pip install -r requirements.txt
```

---

## Step 2 — Create Your Configuration File

```bash
cp .env.example .env
```

Now open the `.env` file in any text editor (Notepad on Windows, TextEdit on Mac) and fill in your values. The sections below explain where to get each key.

---

## Step 3 — Get Your API Keys

### 3A — Claude AI (Required)

1. Go to [console.anthropic.com](https://console.anthropic.com)
2. Sign up or log in
3. Click **API Keys** in the left sidebar
4. Click **Create Key**, give it a name like "Social Media Agent"
5. Copy the key (starts with `sk-ant-`) and paste it into your `.env` file:
   ```
   ANTHROPIC_API_KEY=sk-ant-your-key-here
   ```

---

### 3B — Telegram Bot (Required — this is how you control the agent)

**Create your bot:**
1. Open Telegram and search for **@BotFather**
2. Send `/newbot`
3. Follow the prompts — give your bot a name (e.g., "My Social Agent") and a username (e.g., `mysocial_agent_bot`)
4. BotFather will give you a **token** that looks like `123456789:ABCdef...`
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
4. Under your App → **Keys and Tokens**:
   - Copy **Bearer Token**, **API Key**, **API Key Secret**
   - Under "Access Token and Secret" click **Generate** → copy both values
5. Set your App's **User authentication settings** to have **Read and Write** permissions
6. Paste all 5 values into your `.env` file

---

### 3D — Facebook Page (Optional — enables auto-posting to Facebook)

You need a Facebook Business Page (not a personal profile).

1. Go to [developers.facebook.com](https://developers.facebook.com)
2. Click **My Apps** → **Create App** → choose **Business** type
3. Add the **Facebook Login** product
4. Go to **Tools** → **Graph API Explorer**
5. Select your App, then click **Generate Access Token**
6. Under **Permissions**, add: `pages_manage_posts`, `pages_read_engagement`
7. At the top, switch from "User Token" to **"Page Token"** and select your Page
8. Click Generate → copy the long token
9. To find your Page ID: go to your Facebook Page → **About** → scroll to the bottom
10. Paste both into `.env`:
    ```
    FACEBOOK_ACCESS_TOKEN=your_long_token
    FACEBOOK_PAGE_ID=123456789
    ```

> **Note:** Facebook tokens expire. For a permanent token, follow the [long-lived token guide](https://developers.facebook.com/docs/facebook-login/guides/access-tokens/get-long-lived).

---

### 3E — Instagram (Optional — generates captions for manual posting)

Instagram requires a **Professional account** (Business or Creator) linked to a Facebook Page.

1. In your Facebook Developer App (from 3D above), go to **Graph API Explorer**
2. Add permission: `instagram_basic`, `instagram_content_publish`
3. Generate a **User Access Token** (not page token this time)
4. To find your Instagram Account ID, call this in the Explorer:
   ```
   GET /me/accounts
   ```
   Then for each page, call:
   ```
   GET /{page-id}?fields=instagram_business_account
   ```
5. Paste into `.env`:
    ```
    INSTAGRAM_ACCESS_TOKEN=your_token
    INSTAGRAM_ACCOUNT_ID=your_instagram_id
    ```

> **Note:** Instagram currently requires an image to post to the feed. The agent generates the caption — you pair it with a photo. Future versions will integrate image generation.

---

### 3F — LinkedIn (Optional — enables auto-posting)

1. Go to [developer.linkedin.com](https://developer.linkedin.com)
2. Click **Create App** — use your LinkedIn company page or your own profile
3. Under **Products**, request access to **Share on LinkedIn** and **Sign In with LinkedIn**
4. Go to **Auth** tab → OAuth 2.0 tools → click **Request access token**
5. Authorize with scopes: `w_member_social`, `r_liteprofile`
6. Copy the **Access Token**
7. To get your Person URN, call: `https://api.linkedin.com/v2/me` with the token
   — it returns your ID, and your URN is `urn:li:person:YOUR_ID`
8. Paste into `.env`:
    ```
    LINKEDIN_ACCESS_TOKEN=your_token
    LINKEDIN_PERSON_URN=urn:li:person:XXXXXXXX
    ```

> **Note:** LinkedIn tokens expire after 60 days. Set a reminder to refresh it.

---

### 3G — TikTok and YouTube (Script generation — no API key needed)

The agent **automatically generates scripts and captions** for both platforms.

- **TikTok**: Record your video using the script, then post via the TikTok app. Or use [Buffer](https://buffer.com) or [Later](https://later.com) to schedule.
- **YouTube Long-Form**: Record using the script. Use YouTube Studio to upload, and paste the generated title/description.
- **YouTube Shorts**: Record a vertical video under 60 seconds. Upload as a Short.

---

## Step 4 — Fill In Your Brand Info

In your `.env` file, update the brand section:

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

The more specific you are about your audience and voice, the better the content will be.

**Timezone options:** `America/Los_Angeles`, `America/Chicago`, `America/New_York`, `Europe/London`, `Europe/Paris`, `Asia/Dubai`, `Asia/Singapore`

---

## Step 5 — Start the Agent

Open a terminal in the `social-media-agent` folder and run:

```bash
python main.py
```

You should see:
```
[INFO] Database ready.
[INFO] Scheduler started.
[INFO] Bot running. Open Telegram and send /generate to create content now.
```

Open Telegram, find your bot (search by the username you created), and send:
```
/start
```

Then try:
```
/generate
```

The agent will generate content for all 7 platforms and send you drafts to review!

---

## Daily Usage

| Command | What it does |
|---|---|
| `/generate` | Auto-pick a topic and generate content for all platforms |
| `/topic 5 lessons from my first failed startup` | Generate content for your specific topic |
| `/pending` | See posts waiting for your approval |
| `/recent` | See what's been posted recently |

**When reviewing a draft:**
- **✅ Approve & Post** — publishes immediately to that platform
- **✏️ Edit** — sends edit mode; type your revised content and it will ask you to confirm
- **🔄 Regenerate** — Claude writes a completely new version
- **❌ Skip** — discards this draft

---

## Running 24/7 (So It Posts Every Morning)

To keep the agent running continuously:

**Option A — Simple (Mac/Linux):** Run in the background with:
```bash
nohup python main.py &
```

**Option B — Recommended:** Deploy to [Railway](https://railway.app) (free tier available):
1. Push this folder to a GitHub repository
2. Connect Railway to that repo
3. Add all your `.env` values in Railway's environment variables tab
4. Deploy — it runs 24/7 automatically

**Option C:** Deploy to any VPS (DigitalOcean, Hetzner, Linode) using `screen` or `systemd`.

---

## Troubleshooting

**Bot doesn't respond:**
- Make sure the agent is running (`python main.py`)
- Check that `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID` are correct in `.env`
- Send `/start` to the bot first

**Content generation fails:**
- Check `ANTHROPIC_API_KEY` is valid (test at console.anthropic.com)
- Make sure you have API credits

**Twitter posting fails:**
- Your Twitter app needs **Read and Write** permissions (not just Read)
- You may need to regenerate access tokens after changing permissions

**LinkedIn token expired:**
- LinkedIn tokens last 60 days. Repeat Step 3F to get a fresh token.

**Facebook token expired:**
- Facebook short-lived tokens last 1-2 hours. Create a long-lived token (see Step 3D note).

---

## Content Platform Notes

| Platform | What the agent does |
|---|---|
| Twitter/X | Writes and posts full threads automatically |
| LinkedIn | Writes and posts professional thought-leadership posts |
| Facebook | Writes and posts to your Page |
| Instagram | Writes the caption — you add an image and post |
| TikTok | Writes the script and caption — you record and post |
| YouTube Long-Form | Writes title, description, and full script — you record and upload |
| YouTube Shorts | Writes the short script — you record and upload |
