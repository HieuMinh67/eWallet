import json

import requests as requests


def test_merchant_signup():
    # GIVEN
    payload = json.dumps({
        "merchantName": "Pillow Store",
        "merchantUrl": "pillow.net"
    })
    headers = {
        'Content-Type': 'application/json'
    }

    # WHEN
    response = requests.post(url="http://localhost:8000/merchant/signup", headers=headers, data=payload)

    # THEN
    actual_result = response.json()
    expected_result = {
        "merchantName": "Pillow Store",
        "accountId": actual_result.get("accountId"),
        "merchantId": actual_result.get("merchantId"),
        "apiKey": actual_result.get("apiKey"),
        "merchantUrl": "pillow.net"
    }
    assert expected_result == actual_result
