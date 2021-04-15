from dotenv import load_dotenv
import os

load_dotenv()

_bot_token = os.environ["BOT_TOKEN"]

_admin_id = os.environ["ADMIN_ID"]

_announce_channel = os.environ["ANNOUNCE_CHANNEL"]
_display_channel = os.environ["DISPLAY_CHANNEL"]
_detail_channel = os.environ["DETAIL_CHANNEL"]


def bot_token():
    return _bot_token


def admin_id():
    return _admin_id


def announce_channel():
    return _announce_channel


def display_channel():
    return _display_channel


def detail_channel():
    return _detail_channel
