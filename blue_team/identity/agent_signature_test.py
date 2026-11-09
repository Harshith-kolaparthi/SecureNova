import json 
from pathlib import Path
import base64 

from cryptography.hazmat.primitives import serialization
from cryptography.exceptions import InvalidSignature 


# -------------------------------------------------
# SECURENOVA - Ed25519 AGENT MESSAGE VERIFICATION
# -------------------------------------------------

BASE_DIR = Path(__file__).resolve().parent 
KEY_DIR = BASE_DIR / "keys"

PRIVATE_KEY_PATH = KEY_DIR / "agent_a_private.pem"
PUBLIC_KEY_PATH = KEY_DIR / "agent_a_public.pem"


#Convert message into consistent bytes before singing
def canonical_message(message) :
    return json.dumps(
        message,
        sort_keys=True,
        separators=(",", ":")
    ).encode("utf-8")


#Load Agent A's private key and Agent B's public key
def load_keys():

    private_key = serialization.load_pem_private_key(
        PRIVATE_KEY_PATH.read_bytes(),
        password=None
    )

    public_key = serialization.load_pem_public_key(
        PUBLIC_KEY_PATH.read_bytes()
    )

    return private_key, public_key


#Agent A sings its outgoing message
def sign_message(message, private_key):

    signature = private_key.sign(
        canonical_message(message)
    )

    return base64.b64encode(signature).decode("ascii")


# Agent B verifies the received message.
def verify_message(message, signature_text, public_key):

    signature = base64.b64decode(
        signature_text,
        validate=True
    )

    try:
        public_key.verify(
            signature,
            canonical_message(message)
        )

        return True

    except InvalidSignature:
        return False


if __name__ == "__main__":

    print("=" * 65)
    print(" SECURENOVA - ED25519 AGENT MESSAGE SECURITY TEST")
    print("=" * 65)

    # Load previously generated keys.
    private_key, public_key = load_keys()

    print("\n[1] KEY FILES")
    print("Private key loaded:", PRIVATE_KEY_PATH.exists())
    print("Public key loaded:", PUBLIC_KEY_PATH.exists())

    # Agent A creates an outgoing message.
    original_message = {
        "sender_id": "agent-orchestrator-01",
        "recipient_id": "agent-worker-02",
        "message_id": "MSG-001",
        "action": "change_demo_account_role",
        "account_id": "DEMO-1001",
        "new_role": "admin"
    }

    print("\n[2] ORIGINAL AGENT MESSAGE")
    print(json.dumps(original_message, indent=4))

    # Agent A signs the message.
    signature = sign_message(
        original_message,
        private_key
    )

    print("\n[3] DIGITAL SIGNATURE GENERATED")
    print("Signature algorithm: Ed25519")
    print("Signature generated successfully.")

    # Agent B verifies the original message.
    print("\n[4] VERIFY ORIGINAL MESSAGE")

    original_valid = verify_message(
        original_message,
        signature,
        public_key
    )

    print("Signature verification:", original_valid)

    if original_valid:
        print("RESULT: ORIGINAL MESSAGE ACCEPTED")

    # Simulate an attacker changing one character.
    tampered_message = original_message.copy()

    tampered_message["new_role"] = "user"

    print("\n[5] TAMPERED AGENT MESSAGE")
    print(json.dumps(tampered_message, indent=4))

    # Agent B verifies the modified message using
    # the original signature.
    print("\n[6] VERIFY TAMPERED MESSAGE")

    try:
        public_key.verify(
            base64.b64decode(signature),
            canonical_message(tampered_message)
        )

        print("RESULT: MESSAGE ACCEPTED")

    except InvalidSignature as error:

        print("ERROR TYPE:", type(error).__name__)
        print("ERROR: Signature verification failed.")
        print("RESULT: TAMPERED MESSAGE REJECTED")
        print("SECURITY ALERT: Message integrity compromised.")

    print("\n" + "=" * 65)
    print("ED25519 SIGNATURE VERIFICATION TEST COMPLETED")
    print("=" * 65)