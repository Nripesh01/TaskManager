import requests

access_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzY1MjA1NzExLCJpYXQiOjE3NjUyMDU0MTEsImp0aSI6ImI5ZTkxNzI0YWYyYTQyOWRhNWJhNzkyY2UxYTcyNDcyIiwidXNlcl9pZCI6IjEifQ.n12EIU7WPWfMCGP_EjGv4TsSup2mXyz8NNUXxw7g2G8"

headers = {
    "Authorization": f"Bearer {access_token}"
}

response = requests.get("http://127.0.0.1:8000/list/", headers=headers)

print("Status code:", response.status_code)
print("Response text:", response.text)
