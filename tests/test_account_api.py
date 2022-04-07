import json

import requests as requests


def test_create_account():
    # GIVEN
    payload = json.dumps({
        "accountType": "personal"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/account", headers=headers, data=payload)

    # THEN
    actual_result = response.json()
    expected_result = {
        "accountId": actual_result.get("accountId"),
        "accountType": "personal",
        "balance": 0
    }
    assert expected_result == actual_result


def test_account_top_up(personal_account):
    # GIVEN
    payload = json.dumps({
        "accountId": str(personal_account.account_id),
        "amount": 1.1
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # WHEN
    response = requests.post(url=f"http://localhost:8000/account/{personal_account}/topup", headers=headers,
                             data=payload)

    # THEN
    actual_result = response.status_code
    assert 200 == actual_result


# TODO: add case for merchant and issuer
def test_get_account_token(personal_account):
    # WHEN
    personal_account_id = str(personal_account.account_id)
    response = requests.get(url=f"http://localhost:8000/account/{personal_account_id}/token")

    # THEN
    assert 200 == response.status_code
    assert isinstance(response.content, bytes)
    # TODO: add check decode
