from dataclasses import dataclass
from uuid import UUID

from app.entities.merchant import Merchant
from app.entities.transaction import Transaction


@dataclass
class TransactionCreateBase:
    merchant_id: str
    amount: float
    extra_data: str
    outcome_account: str


@dataclass
class TransactionCreateRequest(TransactionCreateBase):
    @classmethod
    def from_request(cls, data):
        return cls(
            merchant_id=data.get("merchantId"),
            amount=data.get("amount"),
            extra_data=data.get("extraData"),
            outcome_account=data.get("outcomeAccount")
        )

    def to_entity(self) -> Transaction:
        merchant = Merchant.find_by_id(UUID(self.merchant_id))
        return Transaction(
            merchant=merchant,
            amount=self.amount,
            income_account=merchant.account,
            extra_data=self.extra_data,
        )


@dataclass
class TransactionCreateResponse(TransactionCreateBase):
    transaction_id: str
    income_account: str
    signature: str
    status: str

    @classmethod
    def from_entity(cls, transaction: Transaction):
        return cls(
            merchant_id=str(transaction.merchant.merchant_id),
            amount=transaction.amount,
            extra_data=transaction.extra_data,
            outcome_account=str(transaction.outcome_account.account_id) if transaction.outcome_account else None,
            transaction_id=str(transaction.transaction_id),
            income_account=str(transaction.income_account.account_id),
            signature=transaction.signature,
            status=transaction.status.name
        )

    def to_response(self):
        return {
            "transactionId": self.transaction_id,
            "merchantId": self.merchant_id,
            "incomeAccount": self.income_account,
            "outcomeAccount": self.outcome_account,
            "amount": self.amount,
            "extraData": self.extra_data,
            "signature": self.signature,
            "status": self.status
        }
