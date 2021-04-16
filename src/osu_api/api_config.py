from dotenv import dotenv_values

configs = dotenv_values("../../.env")

_client_id = int(configs["CLIENT_ID"])
_client_secret = str(configs["CLIENT_SECRET"])


def client_id() -> int:
    return _client_id


def client_secret() -> str:
    return _client_secret
