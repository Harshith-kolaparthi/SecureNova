
import os
from functools import wraps
from pathlib import Path 

import jwt
import requests

from flask import (
    Flask, render_template, redirect, url_for,
    session, jsonify, request
)
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv
from jwt import PyJWKClient

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET_KEY"]

DOMAIN = os.environ["AUTH0_DOMAIN"]
CLIENT_ID = os.environ["AUTH0_CLIENT_ID"]
CLIENT_SECRET = os.environ["AUTH0_CLIENT_SECRET"]
AUDIENCE = os.environ["AUTH0_AUDIENCE"]

ISSUER = f"https://{DOMAIN}/"
JWKS_URL = f"https://{DOMAIN}/.well-known/jwks.json"

oauth = OAuth(app)

oauth.register(
    name="auth0",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    server_metadata_url=f"{ISSUER}.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid profile email read:ai-data write:admin offline_access",
        "code_challenge_method": "S256",
    },
)

jwks_client = PyJWKClient(JWKS_URL)


def verify_access_token(token):
    signing_key = jwks_client.get_signing_key_from_jwt(token)

    payload = jwt.decode(
        token,
        signing_key.key,
        algorithms=["RS256"],
        audience=AUDIENCE,
        issuer=ISSUER,
    )

    return payload


def require_scope(required_scope):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):

            auth_header = request.headers.get("Authorization", "")

            if not auth_header.startswith("Bearer "):
                return jsonify({"error": "Missing bearer token"}), 401

            token = auth_header.split(" ", 1)[1]

            try:
                claims = verify_access_token(token)
            except jwt.PyJWTError:
                return jsonify({"error": "Invalid or expired token"}), 401
            except Exception:
                return jsonify({"error": "Token validation failed"}), 401

            granted_scopes = claims.get("scope", "").split()

            if required_scope not in granted_scopes:
                return jsonify({
                    "error": "Insufficient permissions",
                    "required_scope": required_scope
                }), 403

            request.jwt_claims = claims
            return function(*args, **kwargs)

        return wrapper
    return decorator


@app.route("/")
def home():
    return render_template(
        "index.html",
        user=session.get("user")
    )


@app.route("/login")
def login():
    return oauth.auth0.authorize_redirect(
        redirect_uri=os.getenv("AUTH0_CALLBACK_URL"),
        audience=os.getenv("AUTH0_AUDIENCE"),
        scope="openid profile email read:ai-data offline_access"
    )


@app.route("/callback")
def callback():
    token = oauth.auth0.authorize_access_token()

    session["user"] = token.get("userinfo", {})
    session["access_token"] = token["access_token"]

    refresh_token=token.get("refresh_token")

    if refresh_token:
        from pathlib import Path
        token_file=Path("/tmp/securenova_refresh_token.txt")
        token_file.write_text(refresh_token)
        token_file.chmod(0o600)

        print("Refresh token received and saved securely for testing")
    else :
        print("Refresh token was not received")


    print("\nRefresh token received:", bool(refresh_token))

    print("\n=======ACCESS TOEKN =======")
    print(token["access_token"])
    print("====================\n")

    print("\n======= ID TOKEN ======")
    print(token.get("id_token"))
    print("====================\n")

    return redirect(url_for("home"))


@app.route("/logout")
def logout():
    session.clear()

    return redirect(
        f"https://{DOMAIN}/v2/logout?"
        f"client_id={CLIENT_ID}&"
        f"returnTo={url_for('home', _external=True)}"
    )


@app.route("/chat", methods=["POST"])
@require_scope("read:ai-data")
def chat():
    data = request.get_json(silent=True) or {}
    message = data.get("message", "")

    if not message.strip():
        return jsonify({"error": "Message is required"}), 400

    return jsonify({
        "message": message,
        "reply": "SecureNova AI received your message.",
        "identity": request.jwt_claims.get("sub")
    })


@app.route("/admin", methods=["GET"])
@require_scope("write:admin")
def admin():
    return jsonify({
        "message": "Admin access granted."
    })


@app.route("/chat-ui", methods=["POST"])
def chat_ui():
    if "access_token" not in session:
        return redirect(url_for("login"))

    # This demonstration reuses the same API authorization rules.
    token = session["access_token"]

    try:
        claims = verify_access_token(token)
    except Exception:
        session.clear()
        return redirect(url_for("login"))

    if "read:ai-data" not in claims.get("scope", "").split():
        return "You do not have permission to use the chat.", 403

    message = request.form.get("message", "").strip()

    return jsonify({
        "reply": f"SecureNova AI received: {message}"
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
