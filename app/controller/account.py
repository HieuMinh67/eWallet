from app.constants import INTERNAL_SERVER_ERROR, NOT_FOUND
from app.entities.account import Account
from app.schemas.account import TopUpRequest


class AccountController:

    @staticmethod
    def create_account(request_data, **kwargs):
        account = Account.from_dict(request_data)
        result = account.save()
        if not result:
            return INTERNAL_SERVER_ERROR
        return 200, account.to_dict()

    @staticmethod
    def get_token(account_id, **kwargs):
        account = Account.get_by_id(account_id=account_id)
        if not account:
            return NOT_FOUND
        token = account.generate_jwt_token()
        return 200, token

    @staticmethod
    def account_top_up(request_data, account_id):
        top_up_usecase_input = TopUpRequest.from_request(data=request_data)

        # TODO: subtract issuer account amount
        # issuer_account = Account.get_by_id(account_id=account_id)

        personal_account = Account.get_by_id(account_id=top_up_usecase_input.account_id)
        personal_account.balance += top_up_usecase_input.amount
        result = personal_account.update()
        if not result:
            return INTERNAL_SERVER_ERROR
        return 200, ""
