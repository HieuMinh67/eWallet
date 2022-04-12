from dataclasses import dataclass

from app.entities.account import Account, AccountType
from app.entities.merchant import Merchant


@dataclass
class MerchantCreateBase:
    merchant_name: str
    merchant_url: str


@dataclass
class MerchantCreateRequest(MerchantCreateBase):
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

    @classmethod
    def from_entity(cls, entity):
        return cls(
            merchant_id=str(entity.merchant_id),
            merchant_name=entity.name,
            account_id=str(entity.account.account_id),
            api_key=str(entity.api_key),
            merchant_url=entity.url
        )

    def to_response(self):
        return {
            "merchantName": self.merchant_name,
            "accountId": self.account_id,
            "merchantId": self.merchant_id,
            "apiKey": self.api_key,
            "merchantUrl": self.merchant_url
        }
