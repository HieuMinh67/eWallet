from app.constants import INTERNAL_SERVER_ERROR
from app.schemas.transaction import TransactionCreateRequest, TransactionCreateResponse
from app.utils import token_required


class TransactionController:
    @staticmethod
    def create(request_data, *args, **kwargs):
        transaction_usecase_input = TransactionCreateRequest.from_request(request_data)

        # TODO: validate usecase input
        # result = transaction_usecase_input.validate()
        # if result is False:
        #     return BAD_REQUEST

        try:
            transaction = transaction_usecase_input.to_entity()
            transaction.save()
        except Exception:
            return INTERNAL_SERVER_ERROR

        transaction_usecase_output = TransactionCreateResponse.from_entity(transaction)
        return 200, transaction_usecase_output.to_response()
