import os
import requests
from getpass import getpass
from dotenv import load_dotenv
from pathlib import Path


# Load Auth0 application configuration.
BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

DOMAIN = os.getenv("AUTH0_DOMAIN")
CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

if not all([DOMAIN, CLIENT_ID, CLIENT_SECRET]):
    raise RuntimeError(
        "Missing Auth0 configuration in .env"
    )

TOKEN_URL = f"https://{DOMAIN}/oauth/token"


def exchange_refresh_token(refresh_token):

    response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "refresh_token",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "refresh_token": refresh_token
        },
        timeout=30
    )

    try:
        result = response.json()
    except ValueError:
        result = {}

    return response.status_code, result


print("=" * 65)
print(" SECURENOVA - AUTH0 REFRESH TOKEN ROTATION TEST")
print("=" * 65)

# Obtain the genuine refresh token securely without echoing it.
TOKEN_FILE=Path("/tmp/securenova_refresh_token.txt")

if not TOKEN_FILE.exists():
    raise FileNotFoundError (
        "Refresh token file not found. Please log in through app.py first"
    )
old_refresh_token = TOKEN_FILE.read_text().strip()

if not old_refresh_token:
    raise RuntimeError("Refresh token file is empty")

print("\nOriginal refresh token loaded securely.")


# First exchange: RT1 should be rotated.
print("\n[1] EXCHANGING ORIGINAL REFRESH TOKEN")

status, result = exchange_refresh_token(old_refresh_token)

if status != 200:
    print("First exchange failed.")
    print("HTTP status:", status)
    print("Auth0 error:", result.get("error", "unknown"))
    print("Description:", result.get("error_description", "not provided"))
    raise SystemExit(1)

new_refresh_token = result.get("refresh_token")

if not new_refresh_token:
    print("No replacement refresh token was returned.")
    print("Check that rotation is enabled for this application.")
    raise SystemExit(1)

print("First exchange successful.")
print("New access token issued:", bool(result.get("access_token")))
print("New refresh token issued: True")
print("Old refresh token should now be invalidated.")

# Second exchange: replay the original RT1.
print("\n[2] REPLAYING THE OLD REFRESH TOKEN")

replay_status, replay_result = exchange_refresh_token(
    old_refresh_token
)

if replay_status == 200:
    print("WARNING: Old refresh token was accepted.")
    print("Check the configured reuse interval and rotation settings.")

else:
    print("OLD REFRESH TOKEN REJECTED")
    print("HTTP status:", replay_status)
    print("Auth0 error:", replay_result.get("error", "unknown"))
    print(
        "Error description:",
        replay_result.get("error_description", "not provided")
    )
    print("RESULT: REPLAY ATTEMPT FAILED AS EXPECTED")

print("\n" + "=" * 65)
print("REFRESH TOKEN REPLAY TEST COMPLETED")
print("=" * 65)