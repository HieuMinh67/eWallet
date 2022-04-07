import uuid
from functools import wraps

from app.constants import UNAUTHORIZED


def generate_uuid() -> uuid.UUID:
    return uuid.uuid4()


def token_required(f):
    @wraps(f)
    def check_token(self, *args, **kwargs):
        token = kwargs.get("headers", dict()).get("Authentication")
        if not token:
            return UNAUTHORIZED
        return f(*args, **kwargs)

    return check_token
