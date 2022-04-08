import json

import requests as requests

from app.entities.transaction import TransactionStatus


def test_create_transaction(merchant, merchant_account, merchant_token, extra_data):
    # GIVEN
    payload = json.dumps({
        "merchantId": str(merchant.merchant_id),
        "amount": 100,
        "extraData": extra_data,
    })
    headers = {
        'Content-Type': 'application/json',
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
        'Content-Type': 'application/json',
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


def test_verify_transaction(confirmed_transaction, personal_account_token):
    # GIVEN
    payload = json.dumps({
        "transactionId": str(confirmed_transaction.transaction_id)
    })
    headers = {
        'Content-Type': 'application/json',
        'Authentication': personal_account_token
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/verify", headers=headers, data=payload)

    # THEN
    actual = response.status_code
    assert 200 == actual


def test_cancel_transaction(confirmed_transaction, personal_account_token):
    # GIVEN
    payload = json.dumps({
        "transactionId": str(confirmed_transaction.transaction_id)
    })
    headers = {
        'Content-Type': 'application/json',
        'Authentication': personal_account_token
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/transaction/cancel", headers=headers, data=payload)

    # THEN
    actual = response.status_code
    assert 200 == actual
