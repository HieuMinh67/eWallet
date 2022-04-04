import uuid
from dataclasses import dataclass, field

from enum import Enum, auto


@dataclass
class AccountType(Enum):
    """
    Merchant: là account được tạo ra khi 1 merchant được đăng ký dùng để quản lý doanh thu của 1 cửa hàng
    Personal: là account của người dùng để thanh toán
    Issuer: là account được cấp phát cho các ngân hàng, các điểm thu tiền. Đây là loại account có quyền thực hiện gọi lệnh nạp tiền vài tài khoản
    """
    PERSONAL = auto()
    MERCHANT = auto()
    ISSUER = auto()


@dataclass
class Account:
    """Account - đối tượng để e-Wallet quản lý tài khoản người dùng

    :param account_id: The account_id of this Account.
    :param account_type: The account_type of this Account.
    :param balance: The balance of this Account.
    """
    account_type: AccountType
    balance: float
    account_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
