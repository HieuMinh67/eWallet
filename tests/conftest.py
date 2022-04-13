import random
import string

import pytest

from app.entities.account import Account, AccountType
from app.entities.merchant import Merchant
from app.entities.transaction import Transaction, TransactionStatus
from app.utils import generate_api_key

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
        url=f"fruit{generate_api_key()}.org",
        account=merchant_account
    ).save()


@pytest.fixture
def merchant_token(merchant_account):
    return merchant_account.generate_jwt_token()


@pytest.fixture
def order_id():
    order_id_list = (
        "fded20e6-9516-4e92-8103-56fe853eed55",
        "9fe01ea8-2762-4bea-aebc-22b203368f80",
        "c327a240-12c0-4267-9569-a748fd3e6b08",
        "0713a03f-cb9c-4fe7-87fc-c2f24f2fe349",
        "0e570617-940a-451f-9f69-a8cea821c6f9",
        "35d3215d-d4e3-49d4-90a8-cdb7d9b4c95d",
        "934f67eb-9d37-4b55-b610-aca8eb3efed0",
    )
    return random.choice(order_id_list)


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
