from dotenv import dotenv_values

configs = dotenv_values("../../.env")

_bot_token = str(configs["BOT_TOKEN"])

_admin_id = int(configs["ADMIN_ID"])

_announce_channel = int(configs["ANNOUNCE_CHANNEL"])
_display_channel = int(configs["DISPLAY_CHANNEL"])
_detail_channel = int(configs["DETAIL_CHANNEL"])


def bot_token() -> str:
    return _bot_token


def admin_id() -> int:
    return _admin_id


def announce_channel() -> int:
    return _announce_channel


def display_channel() -> int:
    return _display_channel


def detail_channel() -> int:
    return _detail_channel
