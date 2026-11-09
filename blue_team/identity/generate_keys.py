from pathlib import Path

from cryptography.hazmat.primitives.asymmetric.ed25519 import (
    Ed25519PrivateKey
)

from cryptography.hazmat.primitives import serialization


# -----------------------------------------
# SecureNova - Ed25519 Key Pair Generation
# -----------------------------------------

BASE_DIR = Path(__file__).resolve().parent
KEY_DIR = BASE_DIR / "keys"

KEY_DIR.mkdir(parents=True, exist_ok=True)


# Generate Ed25519 private key
private_key = Ed25519PrivateKey.generate()

# Derive corresponding public key
public_key = private_key.public_key()


# Serialize private key into PEM format
private_bytes = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# Serialize public key into PEM format
public_bytes = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# Save both key files
private_path = KEY_DIR / "agent_a_private.pem"
public_path = KEY_DIR / "agent_a_public.pem"

private_path.write_bytes(private_bytes)
public_path.write_bytes(public_bytes)


# Verify both files exist
print("=" * 60)
print("     SECURENOVA - ED25519 KEY GENERATION")
print("=" * 60)

print("\nAlgorithm: Ed25519")

print("\nPrivate key file:")
print(private_path)

print("\nPublic key file:")
print(public_path)

print("\nFILE VERIFICATION")

print(
    "Private key created:",
    private_path.exists()
)

print(
    "Public key created:",
    public_path.exists()
)

print("\nSTATUS: SUCCESS")
print("Ed25519 key pair generated successfully.")

print("=" * 60)