import random
import string

import pytest

from app.entities.account import Account, AccountType
from app.entities.merchant import Merchant
from app.entities.transaction import Transaction, TransactionStatus

default_headers = {
    "Content-Type": "application/json"
}


@pytest.fixture
def personal_account():
    # TODO: delete after test
    return Account(account_type=AccountType.personal, balance=1000).save()


@pytest.fixture
def personal_account_token(personal_account):
    return personal_account.generate_jwt_token()


@pytest.fixture
def merchant_account():
    return Account(account_type=AccountType.merchant)


@pytest.fixture
def extra_data():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


@pytest.fixture
def merchant(merchant_account):
    merchant_account.save()
    # TODO: delete after test
    return Merchant(
        name="Fruit Store",
        url="fruit.org",
        account=merchant_account
    ).save()


@pytest.fixture
def merchant_token(merchant_account):
    return merchant_account.generate_jwt_token()


@pytest.fixture
def order_id():
    # order_id_list = (
    #     "795ec7e8-8b44-45b9-8ee8-7e8d8dc8672b",
    #     "ceb9abbf-1fae-49c2-b461-5dec265c8632",
    #     "0a2c7e77-a548-459f-9af0-809ccf6499d4",
    #     "a66ec385-b53e-44f8-a906-993c43d70b59",
    #     "8cd5bcdd-4c4b-4be5-a952-cdf6845c4a2c"
    # )
    # for order_id in order_id_list:
    #     yield order_id
    return "795ec7e8-8b44-45b9-8ee8-7e8d8dc8672b"


@pytest.fixture
def new_transaction(merchant, merchant_account, order_id):
    return Transaction(
        merchant=merchant,
        income_account=merchant_account,
        amount=50,
        extra_data=order_id,
    ).save()


@pytest.fixture
def confirmed_transaction(new_transaction, personal_account):
    new_transaction.status = TransactionStatus.CONFIRMED
    new_transaction.outcome_account = personal_account
    return new_transaction.update()


@pytest.fixture
def low_balance_account():
    return Account(account_type=AccountType.personal).save()
