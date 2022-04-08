import json

import requests as requests

from tests.conftest import default_headers


def test_create_account():
    # GIVEN
    payload = json.dumps({
        "accountType": "personal"
    })

    # WHEN
    response = requests.post(url="http://localhost:8000/account", headers=default_headers, data=payload)

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
    account_id = str(personal_account.account_id)
    payload = json.dumps({
        "accountId": account_id,
        "amount": 1.1
    })

    # WHEN
    response = requests.post(url=f"http://localhost:8000/account/{account_id}/topup",
                             headers=default_headers,
                             data=payload)

    # THEN
    actual_result = response.status_code
    assert 200 == actual_result


# TODO: add case for merchant and issuer
def test_get_account_token(personal_account):
    # WHEN
    personal_account_id = str(personal_account.account_id)
    response = requests.get(url=f"http://localhost:8000/account/{personal_account_id}/token")
    print(response.content)
    # THEN
    assert 200 == response.status_code
    assert isinstance(response.content, bytes)
    # TODO: add check decode
