import aiohttp

from dwp_defines import DiscordLoginData, DWPSettings

"""
Workflow
- authorize discord login page
- get code
- get access_token + refresh_token
"""


async def async_get_request(url, data=None, headers=None):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=7)) as session:
        async with session.get(url=url, data=data, headers=headers) as response:
            return await response.json()


async def async_post_request(url, data=None, headers=None):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=7)) as session:
        async with session.post(url=url, data=data, headers=headers) as response:
            return await response.json()


def get_headers(access_token):
    return {
        "Authorization": f"Bearer {access_token}"
    }


async def get_user_guilds(access_token):
    return await async_get_request(DiscordLoginData.url_discord_user_guilds, headers=get_headers(access_token))


async def get_discord_user_data(access_token):
    """
    Use access token to get personal discord user data
    """
    data = await async_get_request(DiscordLoginData.url_discord_user_data, headers=get_headers(access_token))
    discord_id = data["id"]
    username = data["username"]
    discriminator = data["discriminator"]
    avatar = data["avatar"]
    email = data["email"]


async def refresh_access_token(refresh_token):
    """
    Use refresh_token to get fresh access_token + refresh_token
    """
    data = {
        "client_id": DWPSettings.client_id,
        "client_secret": DiscordLoginData.client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = await async_post_request(DiscordLoginData.url_access_token, data=data, headers=headers)
    access_token = r.get("access_token")
    refresh_token = r.get("refresh_token")


async def get_access_token(code):
    """
    Use code to get the access token
    """
    data = {
        "client_id": DWPSettings.client_id,
        "client_secret": DiscordLoginData.client_secret,
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": DiscordLoginData.redirect_url
    }
    headers = {
        "Content-Type": "application/x-www-form-urlencoded"
    }
    r = await async_post_request(DiscordLoginData.url_access_token, data=data, headers=headers)
    access_token = r.get("access_token")
    refresh_token = r.get("refresh_token")
    return access_token  # , refresh_token
