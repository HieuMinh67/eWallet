from typing import Dict, Any

from app.constants import INTERNAL_SERVER_ERROR
from app.entities.account import Account


class AccountController:

    @classmethod
    def create_account(cls, request_data, **kwargs):
        account = Account.from_dict(request_data)
        result = account.save()
        if not result:
            return INTERNAL_SERVER_ERROR
        return 200, account.to_dict()

    @classmethod
    def get_token(cls, account_id):
        return 200, ""

    @classmethod
    def account_topup(cls, request_data):
        return 200, ""
