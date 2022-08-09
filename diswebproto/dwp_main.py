import webbrowser

from naff import Client
from quart import Quart, request, redirect, url_for, render_template, session

import dwp_secrets
from dwp_api.dwp_api_oauth import get_access_token, get_user_guilds
from dwp_defines import DiscordLoginData, DWPSettings

assert DWPSettings.client_id and DiscordLoginData.client_secret and dwp_secrets.app_secret_key and dwp_secrets.token

app = Quart(__name__)
client = Client()
app.secret_key = dwp_secrets.app_secret_key
app.session_cookie_name = "dwp_session"


@app.before_first_request
async def client_login():
    await client.login(dwp_secrets.token)


@app.route("/", methods=["GET"])
async def index():
    # if request.method == "GET":
    if session.get("access_token"):
        return redirect(url_for("dashboard"))
    else:
        return await render_template("index.html")


@app.route("/on_login_button", methods=["POST"])
async def on_login_button():
    return redirect(DiscordLoginData.client_login_url)


@app.route("/login")
async def app_index():
    session["code"] = request.args.get("code")
    if session["code"]:
        return redirect(url_for("dashboard"))
    else:
        return redirect(url_for("app_error"))


@app.route("/dashboard")
async def dashboard():
    if not session.get("access_token"):
        if not session.get("code"):
            return redirect(url_for("index"))
        session["access_token"] = await get_access_token(session["code"])
    user_guilds = await get_user_guilds(session["access_token"])
    guilds = [[x["name"], x["id"]] for x in user_guilds]
    return await render_template("dashboard.html", guilds=guilds)


@app.route("/on_submit_button", methods=["POST"])
async def on_input_role_name():
    data = await request.form
    role_data = await client.http.create_guild_role(data.get("select_guild"), {"name": data.get("input_role")})
    if role_data:
        return str(role_data)
    else:
        return redirect(url_for("dashboard"))


@app.route("/error")
async def app_error():
    return "<h1>Login failed!</h1>"


if __name__ == "__main__":
    webbrowser.open(DiscordLoginData.url_index)
    app.run(
        host="0.0.0.0" if not DWPSettings.debug else None,
        port=DWPSettings.port,
        debug=DWPSettings.debug
    )
