from passlib.context import CryptContext
from passlib.exc import UnknownHashError
from src.auth import exceptions

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


def hash_password(password: str):
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str):
    if not pwd_context.verify(password, hashed_password):
        raise exceptions.AuthenticationError
    return True
