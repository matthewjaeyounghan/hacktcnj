import json
from os import environ as env
from urllib.parse import quote_plus, urlencode

from authlib.integrations.flask_client import OAuth
from dotenv import find_dotenv, load_dotenv
from flask import Flask, redirect, render_template, session, url_for

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

app = Flask(__name__)
app.secret_key = env.get("APP_SECRET_KEY")
print("APP_SECRET_KEY:", env.get("APP_SECRET_KEY"))

oauth = OAuth(app)

oauth.register(
    "auth0",
    client_id=env.get("AUTH0_CLIENT_ID"),
    client_secret=env.get("AUTH0_CLIENT_SECRET"),
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{env.get("AUTH0_DOMAIN")}/.well-known/openid-configuration',
)

print("AUTH0_CLIENT_ID:", env.get("AUTH0_CLIENT_ID"))
print("AUTH0_CLIENT_SECRET:", env.get("AUTH0_CLIENT_SECRET"))
print("AUTH0_DOMAIN:", env.get("AUTH0_DOMAIN"))

# Controllers API
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/callback", methods=["GET", "POST"])
def callback():
    token = oauth.auth0.authorize_access_token()
    session["user"] = token
    return redirect("/chat")


@app.route("/login")
def login():
    redirect_uri = url_for("callback", _external=True)
    print(f"Login redirecting to: {redirect_uri}")  # Debugging
    return oauth.auth0.authorize_redirect(redirect_uri=redirect_uri)


@app.route("/chat")
def chat():
    return render_template("ready.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect(
        "https://"
        + env.get("AUTH0_DOMAIN")
        + "/v2/logout?"
        + urlencode(
            {
                "returnTo": url_for("home", _external=True),
                "client_id": env.get("AUTH0_CLIENT_ID"),
            },
            quote_via=quote_plus,
        )
    )


if __name__ == "__main__":
    app.run()
