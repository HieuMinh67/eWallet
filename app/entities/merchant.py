import logging
import uuid
from dataclasses import dataclass, field
from uuid import UUID

import psycopg2

from app.db_postgres import PostgreSQL
from app.entities.account import Account, AccountType
from app.utils import generate_uuid, generate_api_key


@dataclass
class Merchant:
    """
    là những cửa hàng online hoặc cửa hàng truyền thống có đăng ký với e-Wallet. Khi đăng ký Merchant e-Wallet sẽ cung cấp 1 account
    """
    name: str
    url: str
    account: Account
    api_key: str = field(default_factory=generate_api_key)
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
            with PostgreSQL() as (db, cursor):
                name_param = (str(self.merchant_id),
                              str(self.account.account_id),
                              self.name,
                              self.url,
                              str(self.api_key))
                cursor.execute(stmt, name_param)
                (result,) = cursor.fetchone()
                db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
        # TODO: handle error if create fail
        return result if result is None else self

    @classmethod
    def find_by_id(cls, _id: UUID, id_type="id") -> 'Merchant':
        # TODO: research about lazy load
        stmt = f"""
        SELECT account_id,
               account.type    account_type,
               account.balance account_balance,
               merchant.id     merchant_id,
               merchant.name,
               merchant.url,
               merchant.api_key
        FROM merchant
                 JOIN account ON merchant.account_id = account.id
        WHERE merchant.{id_type} = %s;
        """
        db_response = None
        try:
            with PostgreSQL() as (_, cursor):
                cursor.execute(stmt, (str(_id),))
                db_response = cursor.fetchone()
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
