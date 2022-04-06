import uuid
from dataclasses import dataclass, field

import psycopg2

from app.entities.account import Account
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
