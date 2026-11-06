import secrets
from bcrypt import checkpw, hashpw, gensalt


def generate_verification_code() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"


def hash_code(code: str) -> str:
    return hashpw(code.encode(), gensalt()).decode()


def verify_code(code: str, hash_code: str) -> bool:
    return checkpw(code.encode(), hash_code.encode())
