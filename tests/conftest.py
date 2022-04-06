import pytest

from app.entities.account import Account, AccountType


@pytest.fixture
def personal_account_id():
    # TODO: delete after test
    return Account(account_type=AccountType.personal).save()
