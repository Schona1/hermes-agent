from constants import SCRIPT_ONLY_PLATFORMS


def get_publisher(platform: str):
    """Return a publisher instance for the platform, or None if script-only."""
    if platform in SCRIPT_ONLY_PLATFORMS:
        return None

    try:
        if platform == "twitter":
            from platforms.twitter import TwitterPublisher
            return TwitterPublisher()
        elif platform == "instagram":
            from platforms.instagram import InstagramPublisher
            return InstagramPublisher()
        elif platform == "linkedin":
            from platforms.linkedin import LinkedInPublisher
            return LinkedInPublisher()
        elif platform == "facebook":
            from platforms.facebook import FacebookPublisher
            return FacebookPublisher()
    except Exception:
        return None

    return None
