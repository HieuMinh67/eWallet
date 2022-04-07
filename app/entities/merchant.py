import logging
import uuid
from dataclasses import dataclass, field
from uuid import UUID

import psycopg2

from app.db_postgres import session
from app.entities.account import Account, AccountType
from app.utils import generate_uuid


@dataclass
class Merchant:
    """
    là những cửa hàng online hoặc cửa hàng truyền thống có đăng ký với e-Wallet. Khi đăng ký Merchant e-Wallet sẽ cung cấp 1 account
    """
    name: str
    url: str
    account: Account
    api_key: uuid.UUID = field(default_factory=generate_uuid)
    merchant_id: uuid.UUID = field(default_factory=generate_uuid)

    def to_usecase_output(self) -> 'MerchantCreateResponse':
        # TODO: find way to fix this circle import
        from app.schemas.merchant import MerchantCreateResponse
        return MerchantCreateResponse(
            merchant_id=str(self.merchant_id),
            merchant_name=self.name,
            account_id=str(self.account.account_id),
            api_key=str(self.api_key),
            merchant_url=self.url
        )

    def save(self):
        stmt = """
            INSERT INTO merchant(id, account_id, name, url, api_key) VALUES (%s, %s, %s, %s, %s) RETURNING id;
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
            name_param = (str(self.merchant_id),
                          str(self.account.account_id),
                          self.name,
                          self.url,
                          str(self.api_key))
            db.execute(stmt, name_param)
            (result,) = db.fetchone()
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
        # TODO: handle error if create fail
        return result

    @classmethod
    def get_by_id(cls, merchant_id: UUID) -> 'Merchant':
        # TODO: research about lazy load
        stmt = """
        SELECT account_id,
               account.type    account_type,
               account.balance account_balance,
               merchant.id     merchant_id,
               merchant.name,
               merchant.url,
               merchant.api_key
        FROM merchant
                 JOIN account ON merchant.account_id = account.id
        WHERE merchant.id = %s;
        """
        db_response = None
        try:
            db = session.cursor()
            db.execute(stmt, (str(merchant_id),))
            db_response = db.fetchone()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)

        # TODO: find better way to do this in case field's order changed
        if db_response is None:
            return 500

        if not db_response[4]:
            return None

        account = Account(
            account_id=UUID(db_response[0]),
            account_type=AccountType(int(db_response[1])),
            balance=float(db_response[2])
        )
        merchant = Merchant(
            merchant_id=UUID(db_response[3]),
            name=db_response[4],
            url=db_response[5],
            api_key=db_response[6],
            account=account
        )
        return merchant
