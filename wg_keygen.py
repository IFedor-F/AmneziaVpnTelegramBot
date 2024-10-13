import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization


def generate_keys():
    private_key = x25519.X25519PrivateKey.generate()

    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    public_key = private_key.public_key()

    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    private_key_base64 = base64.b64encode(private_key_bytes).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key_bytes).decode('utf-8')

    return private_key_base64, public_key_base64


def main():
    private_key_base64, public_key_base64 = generate_keys()
    print(f"{private_key_base64} {public_key_base64}", end='')


if __name__ == '__main__':
    main()
