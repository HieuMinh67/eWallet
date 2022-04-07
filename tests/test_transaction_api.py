import json

import requests as requests

from app.entities.transaction import TransactionStatus


def test_create_transaction(merchant_id, merchant_account, merchant_token, extra_data):
    # GIVEN
    payload = json.dumps({
        "merchantId": merchant_id,
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
        "merchantId": merchant_id,
        "incomeAccount": str(merchant_account.account_id),
        "outcomeAccount": None,
        "amount": 100,
        "extraData": extra_data,
        "signature": actual_result.get("signature"),  # TODO: check it properly
        "status": TransactionStatus.INITIALIZED.name
    }
    assert expected_result == actual_result

def test_confirm_transaction():
    ...
