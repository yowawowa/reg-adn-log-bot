from cryptography.fernet import Fernet
from app.config import settings


def encode_password(password: str) -> bytes:
    """
    Encode a password using a hardcoded Fernet key.

    Args:
        password (str): The password to encode.

    Returns:
        bytes: The encoded password.
    """
    key = settings.FERNET_KEY
    fernet = Fernet(key)
    encoded_password = fernet.encrypt(password.encode())
    return encoded_password



def decode_password(encoded_password: bytes) -> str:
    """
    Decode a password using a hardcoded Fernet key.

    Args:
        encoded_password (bytes): The encoded password to decode.

    Returns:
        str: The decoded password.
    """
    key = settings.FERNET_KEY
    fernet = Fernet(key)
    decoded_password = fernet.decrypt(encoded_password).decode()
    return decoded_password
