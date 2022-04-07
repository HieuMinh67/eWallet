import copy

from app.entities.account import Account, AccountType


def test_get_account_by_id():
    expected = Account(account_type=AccountType.merchant)
    expected.save()

    actual = Account.get_by_id(account_id=expected.account_id)

    assert actual == expected


def test_update_account():
    # GIVEN
    expected = Account(account_type=AccountType.merchant)
    expected.save()

    # WHEN
    update_account = copy.deepcopy(expected)
    update_account.balance += 100
    update_account.account_type = AccountType.personal
    update_account_id = update_account.update()
    actual = Account.get_by_id(account_id=update_account_id)

    # THEN
    assert expected.account_id == actual.account_id
    assert expected.balance - actual.balance != 0
    assert expected.account_type.name != actual.account_type.name
