from __future__ import absolute_import

import uuid
from dataclasses import dataclass, field
from datetime import date, datetime  # noqa: F401
from enum import Enum, auto
from typing import List, Dict  # noqa: F401


class TransactionType(Enum):
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
         chính xác đến order đó.
    :param signature: Là một mã hash md5 (ví dụ: 68b344639ecd4fd9966abda41a59e689) được hash từ payload của Transaction (ngoại trừ signature).
    :param status: The status of this Transaction.  # noqa: E501
    """
    merchant_id: str
    income_account: str
    outcome_account: str
    amount: float
    extra_data: str
    signature: str
    status: TransactionType
    transaction_id: uuid.UUID = field(default_factory=lambda: uuid.uuid4)
