import re
from typing import Union

from django.contrib.auth.hashers import check_password, make_password


def make_hashed_password(password: str) -> str:
    """Hash the password before saving."""
    return make_password(password)


def verify_password(login_password: str, profile_hashed_password: str) -> bool:
    """Verify if the provided password matches the hashed password."""
    return check_password(login_password, profile_hashed_password)


def format_check(password: str) -> Union[bool, str]:
    """Check if the password meets security requirements."""
    validation_rules = [
        (r".{8,}", "Password must be at least 8 characters long"),
        (r"[A-Z]", "Password must contain at least one uppercase letter"),
        (r"[a-z]", "Password must contain at least one lowercase letter"),
        (r"\d", "Password must contain at least one digit"),
        (r"[\W_]", "Password must contain at least one special character"),
    ]
    for pattern, error_message in validation_rules:
        if not re.search(pattern, password):
            return False, error_message
    return True, None
