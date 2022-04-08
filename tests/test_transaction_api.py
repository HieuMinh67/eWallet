import json

import requests as requests

from app.constants import CONTENT_TYPE_JSON
from app.entities.account import Account
from app.entities.transaction import TransactionStatus, Transaction


def test_create_transaction(merchant, merchant_account, merchant_token, extra_data):
    # GIVEN
    payload = json.dumps({
        "merchantId": str(merchant.merchant_id),
        "amount": 100,
        "extraData": extra_data,
    })
    headers = {
        'Content-Type': CONTENT_TYPE_JSON,
        'Authentication': merchant_token
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/create", headers=headers, data=payload)

    # THEN
    actual_result = response.json()
    expected_result = {
        "transactionId": actual_result.get("transactionId"),
        "merchantId": str(merchant.merchant_id),
        "incomeAccount": str(merchant_account.account_id),
        "outcomeAccount": None,
        "amount": 100,
        "extraData": extra_data,
        "signature": actual_result.get("signature"),  # TODO: check it properly
        "status": TransactionStatus.INITIALIZED.name
    }
    assert expected_result == actual_result


def test_confirm_transaction(new_transaction, personal_account_token):
    # GIVEN
    payload = json.dumps({
        "transactionId": str(new_transaction.transaction_id)
    })
    headers = {
        'Content-Type': CONTENT_TYPE_JSON,
        'Authentication': personal_account_token
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/confirm", headers=headers, data=payload)

    # THEN
    expected = {
        "code": "SUC",
        "message": "Transaction was confirmed"
    }
    actual = response.json()
    assert expected == actual


def test_verify_transaction(confirmed_transaction, personal_account):
    transaction_id = str(confirmed_transaction.transaction_id)
    # GIVEN
    payload = json.dumps({
        "transactionId": transaction_id
    })
    headers = {
        'Content-Type': CONTENT_TYPE_JSON,
        'Authentication': personal_account.generate_jwt_token()
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/verify", headers=headers, data=payload)

    # THEN
    actual = response.status_code
    assert 200 == actual
    # when_verify_transaction_transaction_status_will_become_verified_and_balance_is_decrease
    assert Account.get_by_id(personal_account.account_id).balance < personal_account.balance
    assert Transaction.find_by_id(transaction_id).status == TransactionStatus.VERIFIED


def test_cancel_transaction(confirmed_transaction, personal_account_token):
    # GIVEN
    payload = json.dumps({
        "transactionId": str(confirmed_transaction.transaction_id)
    })
    headers = {
        'Content-Type': CONTENT_TYPE_JSON,
        'Authentication': personal_account_token
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/cancel", headers=headers, data=payload)

    # THEN
    actual = response.status_code
    assert 200 == actual


def test_confirm_transaction_with_low_balance(low_balance_account, new_transaction):
    # GIVEN
    payload = json.dumps({
        "transactionId": str(new_transaction.transaction_id)
    })
    headers = {
        'Content-Type': CONTENT_TYPE_JSON,
        'Authentication': low_balance_account.generate_jwt_token()
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/confirm", headers=headers, data=payload)

    # THEN
    actual_status = response.status_code
    actual_text = response.text
    assert 400 == actual_status
    assert "Balance is not enough" == actual_text
