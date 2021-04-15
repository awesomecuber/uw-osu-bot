base_url = "https://osu.ppy.sh/api/v2/"


def token() -> str:
    return "https://osu.ppy.sh/oauth/token"


def user_by_username(username: str) -> str:
    return base_url + f"users/{username}/osu"


def user_by_id(id) -> str:
    return base_url + f"users/{id}"


def recent_scores_by_id(id) -> str:
    return base_url + f"users/{id}/scores/recent"


def beatmapset(id) -> str:
    return base_url + f"beatmapsets/{id}"
