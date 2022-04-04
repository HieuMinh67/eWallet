from dataclasses import dataclass


@dataclass
class MerchantCreateBase:
    merchant_name: str
    merchant_url: str


@dataclass
class MerchantCreateRequest(MerchantCreateBase):
    ...


@dataclass
class MerchantCreateResponse(MerchantCreateBase):
    account_id: str
    merchant_id: str
    api_key: str
