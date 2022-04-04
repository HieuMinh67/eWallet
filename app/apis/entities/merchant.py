import uuid
from dataclasses import dataclass, field

from app.apis.entities.account import Account as AccountEntity


@dataclass
class Merchant:
    """
    là những cửa hàng online hoặc cửa hàng truyền thống có đăng ký với e-Wallet. Khi đăng ký Merchant e-Wallet sẽ cung cấp 1 account
    """
    name: str
    url: str
    account: AccountEntity
    merchant_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
