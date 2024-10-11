import base64
from cryptography.hazmat.primitives.asymmetric import x25519
from cryptography.hazmat.primitives import serialization


def generate_keys():
    # Генерация закрытого ключа
    private_key = x25519.X25519PrivateKey.generate()

    # Получение закрытого ключа в виде байтов
    private_key_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PrivateFormat.Raw,
        encryption_algorithm=serialization.NoEncryption()
    )

    # Получение открытого ключа на основе закрытого
    public_key = private_key.public_key()

    # Получение открытого ключа в виде байтов
    public_key_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.Raw,
        format=serialization.PublicFormat.Raw
    )

    # Преобразование ключей в Base64 формат
    private_key_base64 = base64.b64encode(private_key_bytes).decode('utf-8')
    public_key_base64 = base64.b64encode(public_key_bytes).decode('utf-8')

    return private_key_base64, public_key_base64


def main():
    private_key_base64, public_key_base64 = generate_keys()
    print(f"{private_key_base64}\n{public_key_base64}", end='')  # Возвращаем оба ключа


if __name__ == '__main__':
    main()
