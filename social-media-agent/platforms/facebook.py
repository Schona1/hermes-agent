import requests
from datetime import datetime
from config import FACEBOOK_ACCESS_TOKEN, FACEBOOK_PAGE_ID

GRAPH_URL = "https://graph.facebook.com/v18.0"


class FacebookPublisher:
    def __init__(self):
        self.token = FACEBOOK_ACCESS_TOKEN
        self.page_id = FACEBOOK_PAGE_ID

    def post(self, content: str) -> dict:
        try:
            r = requests.post(
                f"{GRAPH_URL}/{self.page_id}/feed",
                data={"message": content, "access_token": self.token}
            )
            data = r.json()

            if "id" in data:
                return {
                    "success": True,
                    "url": f"https://facebook.com/{data['id']}",
                    "posted_time": datetime.now().isoformat()
                }

            err = data.get("error", {})
            return {"success": False, "error": err.get("message", str(data))}

        except Exception as e:
            return {"success": False, "error": str(e)}

    def post_with_link(self, content: str, link_url: str) -> dict:
        try:
            r = requests.post(
                f"{GRAPH_URL}/{self.page_id}/feed",
                data={"message": content, "link": link_url, "access_token": self.token}
            )
            data = r.json()
            if "id" in data:
                return {
                    "success": True,
                    "url": f"https://facebook.com/{data['id']}",
                    "posted_time": datetime.now().isoformat()
                }
            err = data.get("error", {})
            return {"success": False, "error": err.get("message", str(data))}

        except Exception as e:
            return {"success": False, "error": str(e)}
