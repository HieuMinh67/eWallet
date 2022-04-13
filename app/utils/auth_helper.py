from functools import wraps

from app.constants import UNAUTHORIZED, BAD_REQUEST
from app.entities.account import Account
from app.entities.merchant import Merchant


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


def merchant_token_required(f):
    @wraps(f)
    def check_token(*args, **kwargs):
        token = kwargs.get("headers", dict()).get("Authentication")
        if not token:
            return UNAUTHORIZED

        request_body = kwargs.get("request_data")
        if not request_body:
            return BAD_REQUEST

        merchant_id = request_body.get("merchantId")
        merchant = Merchant.find_by_id(merchant_id)

        account = Account.decode_token(token, secret_key=merchant.api_key)
        kwargs["account"] = account
        return f(*args, **kwargs)

    return check_token
