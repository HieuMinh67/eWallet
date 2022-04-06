from dataclasses import dataclass

from app.entities.account import Account, AccountType
from app.entities.merchant import Merchant


@dataclass
class MerchantCreateBase:
    merchant_name: str
    merchant_url: str


@dataclass
class MerchantCreateRequest(MerchantCreateBase):
    ...

    @classmethod
    def from_request(cls, data):
        return cls(
            merchant_name=data.get("merchantName"),
            merchant_url=data.get("merchantUrl")
        )

    def to_entity(self) -> Merchant:
        return Merchant(
            name=self.merchant_name,
            url=self.merchant_url,
            account=Account(AccountType.merchant)
        )


@dataclass
class MerchantCreateResponse(MerchantCreateBase):
    account_id: str
    merchant_id: str
    api_key: str

    def to_response(self):
        return {
            "merchantName": self.merchant_name,
            "accountId": self.account_id,
            "merchantId": self.merchant_id,
            "apiKey": self.api_key,
            "merchantUrl": self.merchant_url
        }
