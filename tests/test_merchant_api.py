import json

import requests as requests

from app.utils import generate_api_key


def test_merchant_signup():
    # GIVEN
    merchant_url = f"pillow{generate_api_key()}.net"
    payload = json.dumps({
        "merchantName": "Pillow Store",
        "merchantUrl": merchant_url
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
        "merchantUrl": merchant_url
    }
    assert expected_result == actual_result
