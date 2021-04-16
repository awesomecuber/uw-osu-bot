base_url = "https://osu.ppy.sh/api/v2/"


def token() -> str:
    return "https://osu.ppy.sh/oauth/token"


def user_by_username(player_name: str) -> str:
    return base_url + f"users/{player_name}/osu"


def user_by_id(player_id) -> str:
    return base_url + f"users/{player_id}"


def recent_scores_by_id(player_id) -> str:
    return base_url + f"users/{player_id}/scores/recent"


def beatmapset(beatmapset_id) -> str:
    return base_url + f"beatmapsets/{beatmapset_id}"
