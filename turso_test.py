import requests
import os
from dotenv import load_dotenv

load_dotenv()
url = os.getenv("TURSO_DB_URL")
token = os.getenv("TURSO_DB_AUTH_TOKEN")

if not url or not token:
    print("TURSO_DB_URL or TURSO_DB_AUTH_TOKEN is not set. Please check your .env file.")
    exit(1)

# Convert libsql:// to https:// for HTTP API
if url.startswith("libsql://"):
    url = url.replace("libsql://", "https://", 1)

headers = {"Authorization": f"Bearer {token}"}

body = {
    "requests": [
        {"type": "execute", "stmt": {"sql": "SELECT 1"}},
        {"type": "close"}
    ]
}

resp = requests.post(f"{url}/v2/pipeline", headers=headers, json=body)
print(resp.status_code, resp.text)