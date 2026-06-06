import tweepy
from datetime import datetime
from config import (
    TWITTER_API_KEY, TWITTER_API_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_TOKEN_SECRET,
    TWITTER_BEARER_TOKEN
)


class TwitterPublisher:
    def __init__(self):
        self.client = tweepy.Client(
            bearer_token=TWITTER_BEARER_TOKEN,
            consumer_key=TWITTER_API_KEY,
            consumer_secret=TWITTER_API_SECRET,
            access_token=TWITTER_ACCESS_TOKEN,
            access_token_secret=TWITTER_ACCESS_TOKEN_SECRET,
        )

    def _parse_thread(self, content: str) -> list:
        tweets = []
        current = []

        for line in content.split("\n"):
            stripped = line.strip()
            if not stripped:
                continue
            if len(stripped) >= 2 and stripped[0].isdigit() and stripped[1] in "/)":
                if current:
                    tweets.append(" ".join(current))
                rest = stripped[2:].strip()
                current = [rest] if rest else []
            elif stripped.startswith("---"):
                break
            else:
                current.append(stripped)

        if current:
            tweets.append(" ".join(current))

        result = []
        for t in tweets:
            result.append(t[:277] + "..." if len(t) > 280 else t)

        return result if result else [content[:280]]

    def post(self, content: str) -> dict:
        try:
            tweets = self._parse_thread(content)

            if len(tweets) == 1:
                resp = self.client.create_tweet(text=tweets[0])
                tweet_id = resp.data["id"]
                return {
                    "success": True,
                    "url": f"https://twitter.com/i/web/status/{tweet_id}",
                    "posted_time": datetime.now().isoformat()
                }

            first_resp = self.client.create_tweet(text=tweets[0])
            reply_to_id = first_resp.data["id"]
            first_tweet_id = reply_to_id

            for tweet_text in tweets[1:]:
                resp = self.client.create_tweet(
                    text=tweet_text,
                    in_reply_to_tweet_id=reply_to_id
                )
                reply_to_id = resp.data["id"]

            return {
                "success": True,
                "url": f"https://twitter.com/i/web/status/{first_tweet_id}",
                "posted_time": datetime.now().isoformat()
            }

        except Exception as e:
            return {"success": False, "error": str(e)}
