import logging
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum, auto
from uuid import UUID

import jwt
import psycopg2

from app import utils
from app.config import Config
from app.db_postgres import PostgreSQL


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
    """Account - đối tượng để e-Wallet quản lý tài khoản người dùng"""
    account_type: AccountType
    balance: float = 0
    account_id: UUID = field(default_factory=utils.generate_uuid)

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
    def from_db_response(cls, row):
        # TODO: find better way to do this in case field's order changed
        return cls(
            account_id=UUID(row[0]),
            account_type=AccountType(int(row[1])),
            balance=float(row[2])
        )

    @classmethod
    def get_by_id(cls, account_id: UUID):
        stmt = """SELECT * FROM account WHERE id = %s"""
        try:
            with PostgreSQL() as (_, cursor):
                cursor.execute(stmt, (str(account_id),))
                row = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
            return None
        return cls.from_db_response(row)

    def save(self):
        stmt = """
            INSERT INTO account(id, type, balance) VALUES (%s, %s, %s) RETURNING id;
        """
        result = None
        try:
            with PostgreSQL() as (db, cursor):
                cursor.execute(stmt, (str(self.account_id), self.account_type.value, self.balance))
                (result,) = cursor.fetchone()
                db.commit()
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
            with PostgreSQL() as (db, cursor):
                cursor.execute(stmt, (self.account_type.value, self.balance, str(self.account_id)))
                (result,) = cursor.fetchone()
                db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
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
                          key=Config.JWT_SECRET_KEY,
                          algorithm=Config.JWT_ALGORITHM)

    @classmethod
    def decode_token(cls, token: str):
        try:
            payload = jwt.decode(jwt=token, key=Config.JWT_SECRET_KEY, algorithms=Config.JWT_ALGORITHM)
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError as e:
            logging.warning(e)
            return 'Invalid token. Please log in again.'
        account = None
        if account_id := payload.get("sub"):
            account = cls.get_by_id(account_id=account_id)
        # TODO: add case payload invalid
        return account
