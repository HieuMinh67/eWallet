import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from uuid import UUID

import jwt
import psycopg2

from app.db_postgres import session
from app.utils import generate_uuid

JWT_SECRET_KEY = "aslkdmaklmq"  # FIXME: gen key properly
JWT_ALGORITHM = "HS256"


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

    @classmethod
    def get_by_id(cls, account_id: UUID):
        stmt = """SELECT * FROM account WHERE id = %s"""
        result = None
        try:
            conn = psycopg2.connect(
                host="localhost",
                database="e_wallet",
                user="hocvien_dev",
                password="123456"
            )
            db = conn.cursor()
            db.execute(stmt, (str(account_id),))
            db_response = db.fetchone()
            # TODO: find better way to do this in case field's order changed
            result = cls(account_id=UUID(db_response[0]),
                         account_type=AccountType(int(db_response[1])),
                         balance=float(db_response[2]))
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
        return result

    def save(self):
        stmt = """
            INSERT INTO account(id, type, balance) VALUES (%s, %s, %s) RETURNING id;
        """
        result = None
        try:
            db = session.cursor()
            db.execute(stmt, (str(self.account_id), self.account_type.value, self.balance))
            (result,) = db.fetchone()
            session.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
        # TODO: handle error if create fail
        # TODO: return Account instead
        if not result:
            return None
        return self

    def update(self):
        stmt = """
            UPDATE account SET type = %s, balance = %s WHERE id = %s RETURNING id;
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
            db.execute(stmt, (self.account_type.value, self.balance, str(self.account_id)))
            (result,) = db.fetchone()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            logging.warning(e)
        # TODO: handle error if create fail
        # TODO: return Account instead
        return result

    def generate_jwt_token(self):
        payload = {
            'exp': datetime.utcnow() + timedelta(days=1),
            'iat': datetime.utcnow(),
            'sub': str(self.account_id)
        }
        return jwt.encode(payload=payload,
                          key=JWT_SECRET_KEY,
                          algorithm=JWT_ALGORITHM)

    @staticmethod
    def decode_token(token: str):
        try:
            payload = jwt.decode(jwt=token, key=JWT_SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'
        return payload['sub']
