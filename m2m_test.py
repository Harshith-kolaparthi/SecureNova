
import os
import time
from datetime import datetime, timezone

import requests
from dotenv import load_dotenv

load_dotenv()

DOMAIN = os.environ["AUTH0_DOMAIN"]
CLIENT_ID = os.environ["M2M_CLIENT_ID"]
CLIENT_SECRET = os.environ["M2M_CLIENT_SECRET"]
AUDIENCE = os.environ["AUTH0_AUDIENCE"]

TOKEN_URL = f"https://{DOMAIN}/oauth/token"
CHAT_URL = "http://127.0.0.1:5000/chat"


def timestamp():
    return datetime.now(timezone.utc).isoformat()


def get_token():
    response = requests.post(
        TOKEN_URL,
        json={
            "grant_type": "client_credentials",
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "audience": AUDIENCE,
            "scope": "read:ai-data"
        },
        timeout=20
    )

    response.raise_for_status()
    return response.json()


def call_chat(token):
    return requests.post(
        CHAT_URL,
        headers={
            "Authorization": f"Bearer {token}"
        },
        json={
            "message": "Hello from the AI Agent"
        },
        timeout=20
    )


print(f"[{timestamp()}] Requesting M2M access token...")

token_data = get_token()
access_token = token_data["access_token"]
expires_in = token_data["expires_in"]

print(f"[{timestamp()}] Token received.")
print(f"Token lifetime: {expires_in} seconds")

print(f"\n[{timestamp()}] Calling /chat with fresh token...")

first_response = call_chat(access_token)

print("HTTP Status:", first_response.status_code)
print("Response:", first_response.text)

if first_response.status_code != 200:
    raise SystemExit("Fresh token test failed.")

print(f"\n[{timestamp()}] Waiting 65 seconds for expiration...")
time.sleep(65)

print(f"\n[{timestamp()}] Replaying expired token...")

second_response = call_chat(access_token)

print("HTTP Status:", second_response.status_code)
print("Response:", second_response.text)

if second_response.status_code == 401:
    print(f"[{timestamp()}] SUCCESS: Expired token rejected.")
else:
    print(f"[{timestamp()}] TEST FAILED: Expected HTTP 401.")
