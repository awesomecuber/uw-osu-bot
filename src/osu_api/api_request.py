import api_config
import http_request
import token_handler


async def get_token():
    async with http_request.post("https://osu.ppy.sh/oauth/token", {
        "client_id": api_config.client_id(),
        "client_secret": api_config.client_secret(),
        "grant_type": "client_credentials",
        "scope": "public"
    }) as result:
        return result["access_token"]


def headers():
    token = token_handler.get_token()
    return {"Authorization": f"Bearer {token}"}


async def get(url, params):
    async with http_request.get(url, headers(), params) as result:
        return result
