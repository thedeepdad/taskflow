from bcrypt import hashpw, checkpw, gensalt

def hash_password(password: str) -> str: 

    hash_password = hashpw(
        password=password.encode(),
        salt=gensalt()
    ).decode()

    return hash_password

def verify_password(password: str, hashed_password: str) -> bool: 

    result = checkpw(
        password=password.encode(),
        hashed_password=hashed_password.encode()
    )

    return result





