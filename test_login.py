import requests

url = "http://127.0.0.1:8000/login/"

# OAuth2PasswordRequestForm expects form-encoded data
payload = {
    "username": "testuser1",
    "password": "ramesh"
}

headers = {
    "Content-Type": "application/x-www-form-urlencoded"
}

response = requests.post(url, data=payload, headers=headers)

print(response.status_code)
print(response.json())

