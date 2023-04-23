import base64

username = "json"
password = "123"
auth_str = f"{username}:{password}"
auth_bytes = auth_str.encode('ascii')
base64_bytes = base64.b64encode(auth_bytes)
base64_str = base64_bytes.decode('ascii')

print(f"Authorization value: Basic {base64_str}")
