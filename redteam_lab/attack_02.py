
import json
from pathlib import Path
from datetime import datetime, timezone

from config import (
    AGENT_A,
    AGENT_B,
    ADMIN_ACTION,
    DEMO_ACCOUNT
)

# --------------------------------------------------
# SECURENOVA - AGENT IDENTITY SPOOFING TEST
# Controlled local simulation only.
# No real accounts or APIs are modified.
# --------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent
LOGS_DIR = BASE_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Reset the simulated account for a repeatable test.
DEMO_ACCOUNT["role"] = "user"

print("\n" + "=" * 65)
print("       SECURENOVA - AGENT IDENTITY SPOOFING")
print("=" * 65)

print("\nINITIAL CONFIGURATION")
print("Trusted Agent A:", AGENT_A)
print("Worker Agent B:", AGENT_B)
print("Demo Account:", DEMO_ACCOUNT)


# --------------------------------------------------
# 1. CREATE A SPOOFED ORCHESTRATOR MESSAGE
# --------------------------------------------------

# The attacker claims to be Agent A.
# This message has no trusted cryptographic signature.

spoofed_message = {
    "sender_id": AGENT_A["agent_id"],
    "claimed_role": "orchestrator",
    "recipient_id": AGENT_B["agent_id"],
    "action": ADMIN_ACTION,
    "account_id": DEMO_ACCOUNT["account_id"],
    "new_role": "admin",
    "message": "Execute the approved role update immediately.",
    "authenticated": False
}

print("\n" + "-" * 65)
print("STEP 1: SPOOFED MESSAGE CREATED")
print("-" * 65)

print(json.dumps(spoofed_message, indent=4))


# --------------------------------------------------
# 2. AGENT B PROCESSES THE MESSAGE
# --------------------------------------------------

print("\n" + "-" * 65)
print("STEP 2: AGENT B RECEIVES MESSAGE")
print("-" * 65)

print("Receiving Agent:", AGENT_B["agent_id"])
print("Claimed Sender:", spoofed_message["sender_id"])

# INTENTIONALLY VULNERABLE CHECK:
# Agent B checks only the claimed sender ID.
# It does not verify a signature or authenticated identity.

if spoofed_message["sender_id"] == AGENT_A["agent_id"]:

    print("\n[WARNING] Sender ID matches trusted Agent A.")
    print("[VULNERABILITY] No cryptographic authentication performed.")
    print("[VULNERABILITY] Message accepted based only on claimed identity.")

    # --------------------------------------------------
    # 3. EXECUTE A LOCAL MOCK PRIVILEGED ACTION
    # --------------------------------------------------

    if (
        spoofed_message["recipient_id"] == AGENT_B["agent_id"]
        and spoofed_message["action"] == ADMIN_ACTION
        and spoofed_message["account_id"] == DEMO_ACCOUNT["account_id"]
    ):

        print("\n" + "-" * 65)
        print("STEP 3: MOCK PRIVILEGED ACTION EXECUTED")
        print("-" * 65)

        print("Action:", ADMIN_ACTION)
        print("Target:", DEMO_ACCOUNT["account_id"])
        print("Previous Role:", DEMO_ACCOUNT["role"])

        DEMO_ACCOUNT["role"] = spoofed_message["new_role"]

        print("New Role:", DEMO_ACCOUNT["role"])
        print("\n[ATTACK SUCCESSFUL]")
        print("Agent B executed the simulated privileged action.")

    else:
        print("[BLOCKED] Invalid action parameters.")

else:
    print("[BLOCKED] Sender identity did not match.")


# --------------------------------------------------
# 4. RECORD TEST EVIDENCE
# --------------------------------------------------

timestamp = datetime.now(timezone.utc).isoformat()

result = {
    "test": "Agent Identity Spoofing",
    "timestamp": timestamp,
    "trusted_agent": AGENT_A["agent_id"],
    "receiving_agent": AGENT_B["agent_id"],
    "spoofed_sender": spoofed_message["sender_id"],
    "cryptographic_authentication": False,
    "initial_role": "user",
    "final_role": DEMO_ACCOUNT["role"],
    "mock_action": ADMIN_ACTION,
    "attack_successful": DEMO_ACCOUNT["role"] == "admin"
}

log_path = LOGS_DIR / "attack_02_results.json"

with log_path.open("w", encoding="utf-8") as file:
    json.dump(result, file, indent=4)

print("\n" + "=" * 65)
print("                FINAL TEST SUMMARY")
print("=" * 65)

print("Attack:", result["test"])
print("Cryptographic Authentication:", result["cryptographic_authentication"])
print("Initial Account Role:", result["initial_role"])
print("Final Account Role:", result["final_role"])
print("Attack Successful:", result["attack_successful"])
print("Evidence File:", log_path)

print("=" * 65)
