import json

import requests as requests


def test_merchant_signup():
    # GIVEN
    payload = json.dumps({
        "merchantName": "MoMo",
        "merchantUrl": "momo.vn"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/merchant/signup", headers=headers, data=payload)

    # THEN
    actual_result = response.json()
    expected_result = {
        "merchantName": "MoMo",
        "accountId": actual_result.get("accountId"),
        "merchantId": actual_result.get("merchantId"),
        "apiKey": actual_result.get("apiKey"),
        "merchantUrl": "momo.vn"
    }
    assert expected_result == actual_result
