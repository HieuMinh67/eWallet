import asyncio

from app.constants import INTERNAL_SERVER_ERROR, BAD_REQUEST
from app.entities.transaction import Transaction, TransactionStatus
from app.schemas.transaction import TransactionCreateRequest, TransactionCreateResponse
from app.utils.auth_helper import token_required


class TransactionController:
    @classmethod
    @token_required
    def confirm(cls, request_data, **kwargs):
        # get account from token
        confirmed_account = kwargs.get("account")

        # TODO: refactor this (usecase)
        transaction_id = request_data.get("transactionId")

        transaction = Transaction.find_by_id(transaction_id)
        if not transaction:
            return BAD_REQUEST

        transaction.outcome_account = confirmed_account

        return cls.change_status(transaction, status=TransactionStatus.CONFIRMED)

    @classmethod
    @token_required
    def verify(cls, request_data, **kwargs):
        # TODO: refactor this (usecase)
        transaction_id = request_data.get("transactionId")

        transaction = Transaction.find_by_id(transaction_id)
        if not transaction:
            return BAD_REQUEST

        return cls.change_status(transaction, status=TransactionStatus.VERIFIED)

    @classmethod
    @token_required
    def cancel(cls, request_data, **kwargs):
        # TODO: refactor this (usecase)
        transaction_id = request_data.get("transactionId")

        transaction = Transaction.find_by_id(transaction_id)
        if not transaction:
            return BAD_REQUEST

        return cls.change_status(transaction, status=TransactionStatus.CANCELED)

    @classmethod
    async def expire(cls, transaction_id, expired_time: int = 30):
        """

        :param transaction_id:
        :param expired_time: a given time (in seconds).
        """
        await asyncio.sleep(expired_time)
        transaction = Transaction.find_by_id(transaction_id)
        if transaction and transaction.status != TransactionStatus.COMPLETED:
            transaction.status = TransactionStatus.EXPIRED
            transaction.update()

    @classmethod
    def change_status(cls, transaction: Transaction, status: TransactionStatus):
        transaction.status = status
        result = transaction.update()

        if result is None:
            return INTERNAL_SERVER_ERROR

        # TODO: refactor this (usecase)
        return 200, {
            "code": "SUC",
            "message": f"Transaction was {status.name.lower()}"
        }

    @classmethod
    @token_required
    def create(cls, request_data, *args, **kwargs):
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

        asyncio.run(cls.expire(transaction_id=transaction.transaction_id))

        transaction_usecase_output = TransactionCreateResponse.from_entity(transaction)
        return 200, transaction_usecase_output.to_response()
