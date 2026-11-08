
import os

from flask import Flask, redirect, url_for, session
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("FLASK_SECRET_KEY")

oauth = OAuth(app)

domain = os.getenv("AUTH0_DOMAIN")

oauth.register(
    name="auth0",
    client_id=os.getenv("SECOND_CLIENT_ID"),
    client_secret=os.getenv("SECOND_CLIENT_SECRET"),
    server_metadata_url=f"https://{domain}/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email"
    }
)


@app.route("/")
def home():
    user = session.get("user")

    if not user:
        return """
        <h1>SecureNova Second Client</h1>
        <p>Second application for SSO testing.</p>
        <a href="/login">Login with Auth0</a>
        """

    return f"""
    <h1>SecureNova Second Client</h1>
    <h2>Welcome, {user.get('email', 'User')}</h2>
    <p>You are authenticated through Auth0.</p>
    <p>SSO Client 2 login successful!</p>
    <a href="/logout">Logout</a>
    """


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=os.getenv("SECOND_CALLBACK_URL")
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    session["user"] = token.get("userinfo", {})

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
