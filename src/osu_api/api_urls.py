base_url = "https://osu.ppy.sh/api/v2/"


def token():
    return "https://osu.ppy.sh/oauth/token"


def user_by_username(username):
    return base_url + f"users/{username}/osu"


def user_by_id(id):
    return base_url + f"users/{id}"


def recent_scores_by_id(id):
    return base_url + f"users/{id}/scores/recent"


def beatmapset(id):
    return base_url + f"beatmapsets/{id}"
