from functools import wraps

from app.constants import UNAUTHORIZED
from app.entities.account import Account


def token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = kwargs.get("headers", dict()).get("Authentication")
        if not token:
            return UNAUTHORIZED
        account = Account.decode_token(token)
        kwargs["account"] = account
        # TODO: verify token
        return f(*args, **kwargs)

    return check_token
