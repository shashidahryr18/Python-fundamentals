from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding


message = b"Hello Information Security"

with open("message.txt", "wb") as file:
    file.write(message)

print("1. Sample file created: message.txt")

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)

with open("private.pem", "wb") as file:
    file.write(
        private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )
    )

print("2. RSA Private Key generated: private.pem")

public_key = private_key.public_key()

with open("public.pem", "wb") as file:
    file.write(
        public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
    )

print("3. Public Key generated: public.pem")

with open("message.txt", "rb") as file:
    data = file.read()

signature = private_key.sign(
    data,
    padding.PKCS1v15(),
    hashes.SHA256()
)

with open("signature.bin", "wb") as file:
    file.write(signature)

print("4. Digital Signature created: signature.bin")

with open("signature.bin", "rb") as file:
    signature = file.read()

try:
    public_key.verify(
        signature,
        data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    print("5. Signature Verification: Verified OK")

except Exception:
    print("5. Signature Verification: Verification Failed")

with open("message.txt", "ab") as file:
    file.write(b"\nModified Data")

print("6. File modified.")

with open("message.txt", "rb") as file:
    modified_data = file.read()

try:
    public_key.verify(
        signature,
        modified_data,
        padding.PKCS1v15(),
        hashes.SHA256()
    )

    print("7. Modified File Verification: Verified OK")

except Exception:
    print("7. Modified File Verification: Verification Failure")
    
