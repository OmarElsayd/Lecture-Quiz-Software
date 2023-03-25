import hashlib
import re


def get_hashed_password(password: str) -> str:
    """
    Get hashed password
    Args:
        password (str): Password to be hashed

    Returns:
        str: Hashed password
    """
    return hashlib.sha256(password.encode()).hexdigest()


def validate_email(email: str) -> bool:
    """
    Validate email
    Args:
        email (str): Email to be validated

    Returns:
        bool: True if email is valid, False otherwise
    """
    if not email:
        return False
    if not re.match(r"^[a-zA-Z0-9_.+-]+@+stud.uni-due.de", email):
        return False
    return True

def create_quiz_code() -> str:
    """
    Create a random quiz code
    Returns:
        str: Random quiz code
    """
    import random
    import string
    letters = string.ascii_uppercase
    return ''.join(random.choice(letters) for i in range(6))
