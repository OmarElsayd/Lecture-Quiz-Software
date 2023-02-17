import hashlib


def get_hashed_password(password: str) -> str:
    """
    Get hashed password
    Args:
        password (str): Password to be hashed

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()
