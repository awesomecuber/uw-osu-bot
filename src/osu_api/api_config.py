from dotenv import dotenv_values

configs = dotenv_values("../../.env")

_client_id = configs["CLIENT_ID"]
_client_secret = configs["CLIENT_SECRET"]


def client_id():
    return _client_id


def client_secret():
    return _client_secret
