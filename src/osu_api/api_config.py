from dotenv import load_dotenv
import os

load_dotenv()
_client_id = os.environ["CLIENT_ID"]
_client_secret = os.environ["CLIENT_SECRET"]


def client_id():
    return _client_id


def client_secret():
    return _client_secret
