from dataclasses import dataclass


@dataclass
class TopUpRequest:
    account_id: str
    amount: float

    @classmethod
    def from_request(cls, data):
        return cls(
            account_id=data.get("accountId"),
            amount=data.get("amount")
        )
