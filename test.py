# test.py

import requests
import json

url = "http://127.0.0.1:8000/identify"

payload = {
    "email": "doc@future.com",
    "phoneNumber": "1234567890"
}

headers = {
    "Content-Type": "application/json"
}

response = requests.post(url, data=json.dumps(payload), headers=headers)

print("🔍 Status Code:", response.status_code)
print("📦 Response JSON:", json.dumps(response.json(), indent=2))
