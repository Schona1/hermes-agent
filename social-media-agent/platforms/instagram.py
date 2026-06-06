import requests
from datetime import datetime
from config import INSTAGRAM_ACCESS_TOKEN, INSTAGRAM_ACCOUNT_ID

GRAPH_URL = "https://graph.facebook.com/v18.0"


class InstagramPublisher:
    def __init__(self):
        self.token = INSTAGRAM_ACCESS_TOKEN
        self.account_id = INSTAGRAM_ACCOUNT_ID

    def _extract_caption(self, content: str) -> str:
        for marker in ["CONTENT FORMAT", "CAROUSEL", "VISUAL DIRECTION", "If carousel"]:
            idx = content.find(marker)
            if idx != -1:
                content = content[:idx]
        return content.strip()[:2200]

    def post(self, content: str) -> dict:
        caption = self._extract_caption(content)
        return {
            "success": False,
            "error": (
                "Instagram requires an image. Your caption is saved.\n\n"
                "To post: open Instagram, create a post with any image, "
                "and paste the approved caption."
            ),
            "caption": caption
        }

    def post_with_image(self, caption: str, image_url: str) -> dict:
        try:
            r = requests.post(
                f"{GRAPH_URL}/{self.account_id}/media",
                data={"image_url": image_url, "caption": caption[:2200], "access_token": self.token}
            )
            data = r.json()
            if "id" not in data:
                return {"success": False, "error": data.get("error", {}).get("message", "Container failed")}

            container_id = data["id"]

            r2 = requests.post(
                f"{GRAPH_URL}/{self.account_id}/media_publish",
                data={"creation_id": container_id, "access_token": self.token}
            )
            data2 = r2.json()
            if "id" in data2:
                return {
                    "success": True,
                    "url": f"https://instagram.com/p/{data2['id']}",
                    "posted_time": datetime.now().isoformat()
                }
            return {"success": False, "error": data2.get("error", {}).get("message", "Publish failed")}

        except Exception as e:
            return {"success": False, "error": str(e)}
