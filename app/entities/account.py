from dataclasses import dataclass, field
from enum import Enum, auto
from uuid import UUID

import psycopg2

from app.utils import generate_uuid


@dataclass
class AccountType(Enum):
    """
    Merchant: là account được tạo ra khi 1 merchant được đăng ký dùng để quản lý doanh thu của 1 cửa hàng
    Personal: là account của người dùng để thanh toán
    Issuer: là account được cấp phát cho các ngân hàng, các điểm thu tiền. Đây là loại account có quyền thực hiện gọi lệnh nạp tiền vài tài khoản
    """
    personal = auto()
    merchant = auto()
    issuer = auto()


@dataclass
class Account:
    """Account - đối tượng để e-Wallet quản lý tài khoản người dùng

    :param account_id: The account_id of this Account.
    :param account_type: The account_type of this Account.
    :param balance: The balance of this Account.
    """
    account_type: AccountType
    balance: float = 0
    account_id: UUID = field(default_factory=generate_uuid)

    def to_dict(self):
        return {
            "accountId": str(self.account_id),
            "accountType": self.account_type.name,
            "balance": self.balance
        }

    @classmethod
    def from_dict(cls, data) -> 'Account':
        return cls(account_type=AccountType[data.get("accountType")])

    def save(self):
        stmt = """
            INSERT INTO account(id, type, balance) VALUES (%s, %s, %s) RETURNING id;
        """
        result = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="e_wallet",
                user="hocvien_dev",
                password="123456"
            )
            db = conn.cursor()
            db.execute(stmt, (str(self.account_id), self.account_type.value, self.balance))
            (result,) = db.fetchone()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
        # TODO: handle error if create fail
        return result
