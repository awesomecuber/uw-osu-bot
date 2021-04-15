from dotenv import load_dotenv
import os

load_dotenv()
client_id = os.environ["CLIENT_ID"]
client_secret = os.environ["CLIENT_SECRET"]


def client_id():
    return client_id


def client_secret():
    return client_secret
