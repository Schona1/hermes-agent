import requests
from datetime import datetime
from config import LINKEDIN_ACCESS_TOKEN, LINKEDIN_PERSON_URN


class LinkedInPublisher:
    BASE_URL = "https://api.linkedin.com/v2"

    def __init__(self):
        self.headers = {
            "Authorization": f"Bearer {LINKEDIN_ACCESS_TOKEN}",
            "Content-Type": "application/json",
            "X-Restli-Protocol-Version": "2.0.0"
        }
        self.person_urn = LINKEDIN_PERSON_URN

    def post(self, content: str) -> dict:
        try:
            text = content[:3000]

            payload = {
                "author": self.person_urn,
                "lifecycleState": "PUBLISHED",
                "specificContent": {
                    "com.linkedin.ugc.ShareContent": {
                        "shareCommentary": {"text": text},
                        "shareMediaCategory": "NONE"
                    }
                },
                "visibility": {
                    "com.linkedin.ugc.MemberNetworkVisibility": "PUBLIC"
                }
            }

            r = requests.post(f"{self.BASE_URL}/ugcPosts", headers=self.headers, json=payload)

            if r.status_code == 201:
                post_id = r.headers.get("x-restli-id", "")
                return {
                    "success": True,
                    "url": f"https://www.linkedin.com/feed/update/{post_id}",
                    "posted_time": datetime.now().isoformat()
                }

            err = r.json()
            return {"success": False, "error": err.get("message", f"HTTP {r.status_code}")}

        except Exception as e:
            return {"success": False, "error": str(e)}
