"""
VENDOR TOOL ONLY - NOT INCLUDED IN CLIENT EXECUTABLE
Generates RSA-2048 Keypair for WinForge Licensing.
"""

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from pathlib import Path


def generate_rsa_keypair(output_dir: Path):
    """Generates RSA-2048 private and public key Pem files."""
    output_dir.mkdir(parents=True, exist_ok=True)

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048
    )

    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    priv_path = output_dir / "private_key.pem"
    pub_path = output_dir / "public_key.pem"

    with open(priv_path, "wb") as f:
        f.write(private_pem)

    with open(pub_path, "wb") as f:
        f.write(public_pem)

    print(f"[VENDOR TOOL] Keypair generated successfully:\n Private Key: {priv_path}\n Public Key: {pub_path}")
    return priv_path, pub_path


if __name__ == "__main__":
    generate_rsa_keypair(Path("vendor_keys"))
