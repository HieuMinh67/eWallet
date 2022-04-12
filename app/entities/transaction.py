from __future__ import absolute_import

import hashlib
import json
import logging
import uuid
from dataclasses import dataclass, field
from datetime import date, datetime  # noqa: F401
from enum import Enum, auto
from typing import List, Dict, Optional  # noqa: F401
from uuid import UUID

import psycopg2

from app.db_postgres import PostgreSQL
from app.entities.account import Account
from app.entities.merchant import Merchant
from app.utils import generate_uuid


class TransactionStatus(Enum):
    """
    Initialized: transaction đã được tạo (đã xác định số tiền và account thụ hưởng)
    Confirmed: transaction đã được confirm (đã xác định account thanh toán)
    Verified: transaction đã được xác nhận (sẽ được thực hiện thanh toán sau đó)
    Completed: transaction đã hoàn thành, thanh toán thành công
    Expired: transaction đã vượt quá 5 phút nhưng chưa hoàn thành
    Canceled: transaction bị cancel bởi /transaction/cancel
    Failed: transaction bị Fail do balance không đủ
    """
    INITIALIZED = auto()
    CONFIRMED = auto()
    VERIFIED = auto()
    COMPLETED = auto()
    EXPIRED = auto()
    CANCELED = auto()
    FAILED = auto()


@dataclass
class Transaction:
    """Transaction - dùng để quản lý 1 phiên giao dịch

    :param transaction_id: The transaction_id of this Transaction.  # noqa: E501
    :param merchant_id: The merchant_id of this Transaction.  # noqa: E501
    :param income_account: The income_account of this Transaction.  # noqa: E501
    :param outcome_account: The outcome_account of this Transaction.  # noqa: E501
    :param amount: The amount of this Transaction.  # noqa: E501
    :param extra_data: ExtraData có thể là bất cứ thứ gì do hệ thống merchant định nghĩa. Mỗi khi e-Wallet update thông
     tin thay đổi transaction thì cần gửi kèm thông tin extraData. Dữ liệu này không có ý nghĩa trong hệ thống của
      e-Wallet, tuy nhiên sẽ có ý nghĩa ở hệ thống của merchant. Ví dụ: nếu merchant thêm thông tin orderId vào
       extraData, e-Wallet sẽ không hiểu orderId này là gì cả, tuy nhiên khi e-Wallet gửi thông tin transaction về cho
        Merchant, merchant sẽ đọc và biết transaction này đang sử lý cho orderId nào để có thể cập nhật trạng thái
         chính xác đến order đó. -> OrderID
    :param signature: Là một mã hash md5 (ví dụ: 68b344639ecd4fd9966abda41a59e689) được hash từ payload của Transaction (ngoại trừ signature).
    :param status: The status of this Transaction.  # noqa: E501
    """
    merchant: Merchant
    income_account: Account
    amount: float
    extra_data: str
    status: TransactionStatus = TransactionStatus.INITIALIZED
    outcome_account: Optional[Account] = None
    transaction_id: uuid.UUID = field(default_factory=generate_uuid)

    @property
    def signature(self):
        payload = json.dumps({
            "merchantId": str(self.merchant.merchant_id),
            "amount": self.amount,
            "extraData": self.extra_data
        })
        return hashlib.md5(payload.encode("UTF-8")).hexdigest()

    def save(self):
        stmt = """
            INSERT INTO transaction(id,
                                    merchant_id,
                                    extra_data,
                                    signature,
                                    amount,
                                    account_income,
                                    account_outcome,
                                    status) 
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        try:
            with PostgreSQL() as (db, cursor):
                name_param = (str(self.transaction_id),
                              str(self.merchant.merchant_id),
                              self.extra_data,
                              self.signature,
                              self.amount,
                              str(self.merchant.account.account_id),
                              None if not self.outcome_account else str(self.outcome_account.account_id),
                              self.status.value)
                cursor.execute(stmt, name_param)
                (result,) = cursor.fetchone()
                db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            print(e)
            logging.warning(e)
            raise e
        # TODO: handle error if create fail
        return None if result is None else self

    @classmethod
    def find_by_id(cls, transaction_id: str):
        stmt = """SELECT * FROM transaction WHERE id = %s"""
        db_response = None
        try:
            with PostgreSQL() as (_, cursor):
                cursor.execute(stmt, (transaction_id,))
                db_response = cursor.fetchone()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)

        if db_response is None:
            return None

        merchant = Merchant.find_by_id(db_response[1])
        outcome_account = Account.get_by_id(db_response[6]) if db_response[6] is not None else None

        return cls(
            transaction_id=UUID(db_response[0]),
            merchant=merchant,
            extra_data=db_response[2],
            amount=float(db_response[4]),
            income_account=merchant.account,
            outcome_account=outcome_account,
            status=TransactionStatus(db_response[7])
        )

    def update(self):
        stmt = """
            UPDATE transaction
            SET account_outcome = %s,
                status = %s
            WHERE id = %s RETURNING id;
        """
        result = None
        try:
            with PostgreSQL() as (db, cursor):
                cursor.execute(stmt, (str(self.outcome_account.account_id) if self.outcome_account else None,
                                      self.status.value,
                                      str(self.transaction_id)))
                (result,) = cursor.fetchone()
                db.commit()
        except (Exception, psycopg2.DatabaseError) as e:
            logging.warning(e)
        # TODO: handle error if create fail
        # TODO: return Account instead
        return result if result is None else self
