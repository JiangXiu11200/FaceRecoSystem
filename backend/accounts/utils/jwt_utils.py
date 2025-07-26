import datetime
from typing import Union

import jwt
from django.conf import settings

ALLOWED_ALGORITHMS = "RS256"


def generate_access_jwt(user_id: int, account: str, exp_delta_seconds: int = 3600) -> Union[str, None]:
    """Generate a JWT token for the user."""
    payload = {
        "user_id": user_id,
        "account": account,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=exp_delta_seconds),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=ALLOWED_ALGORITHMS)
    return token


def generate_refresh_jwt(user_id: int, account: str, exp_delta_days: int = 3) -> Union[str, None]:
    """Generate a refresh JWT token for the user."""
    payload = {
        "user_id": user_id,
        "account": account,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=exp_delta_days),
        "iat": datetime.datetime.utcnow(),
    }
    token = jwt.encode(payload, settings.JWT_PRIVATE_KEY, algorithm=ALLOWED_ALGORITHMS)
    return token


def verify_access_jwt(token: str) -> Union[dict, None]:
    """Verify the JWT token and return the payload."""
    try:
        payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[ALLOWED_ALGORITHMS])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def verify_refresh_jwt(token: str) -> Union[dict, None]:
    try:
        payload = jwt.decode(token, settings.JWT_PUBLIC_KEY, algorithms=[ALLOWED_ALGORITHMS])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
