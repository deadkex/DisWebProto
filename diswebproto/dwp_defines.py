import dwp_secrets


class DWPSettings:
    client_id = dwp_secrets.client_id
    port = 63883
    debug = True


class DiscordLoginData:
    client_secret = dwp_secrets.client_secret
    url_index = f"http://localhost:{DWPSettings.port}"
    client_login_url = f"https://discord.com/api/oauth2/authorize" \
                       f"?client_id={DWPSettings.client_id}" \
                       f"&redirect_uri=http%3A%2F%2Flocalhost%3A{DWPSettings.port}%2Flogin" \
                       f"&response_type=code&scope=identify%20email%20guilds"
    redirect_url = f"http://localhost:{DWPSettings.port}/login"
    api_endpoint = "https://discord.com/api/v10"
    url_access_token = f"{api_endpoint}/oauth2/token"
    url_discord_user_data = f"{api_endpoint}/users/@me"
    url_discord_user_guilds = f"{api_endpoint}/users/@me/guilds"
