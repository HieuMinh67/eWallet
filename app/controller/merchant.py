from app.constants import INTERNAL_SERVER_ERROR
from app.entities.merchant import Merchant
from app.schemas.merchant import MerchantCreateRequest


class MerchantController:
    @classmethod
    def signup(cls, request_data, **kwargs):
        # TODO: handle wrong input key
        merchant_usecase_input = MerchantCreateRequest.from_request(request_data)
        merchant = merchant_usecase_input.to_entity()
        create_account_result = merchant.account.save()
        if not create_account_result:
            return INTERNAL_SERVER_ERROR

        # TODO: consider using Walrus Operator
        create_merchant_result = merchant.save()
        if not create_merchant_result:
            return INTERNAL_SERVER_ERROR

        merchant_usecase_output = merchant.to_usecase_output()
        return 200, merchant_usecase_output.to_response()
