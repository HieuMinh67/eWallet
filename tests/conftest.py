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
def new_transaction(merchant, merchant_account, extra_data):
    return Transaction(
        merchant=merchant,
        income_account=merchant_account,
        amount=50,
        extra_data=extra_data,
    ).save()


@pytest.fixture
def confirmed_transaction(new_transaction, personal_account):
    new_transaction.status = TransactionStatus.CONFIRMED
    new_transaction.outcome_account = personal_account
    return new_transaction.update()


@pytest.fixture
def low_balance_account():
    return Account(account_type=AccountType.personal).save()
