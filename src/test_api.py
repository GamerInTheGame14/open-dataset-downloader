
import requests

API_URL = "https://api.gsa.gov/technology/datagov/v4/search"

headers = {
    "X-Api-Key": "DEMO_KEY"
}

params = {
    "q": "climate",
    "per_page": 5
}

response = requests.get(
    API_URL,
    headers=headers,
    params=params,
    timeout=30
)

print("Status code:", response.status_code)

response.raise_for_status()

data = response.json()

for index, dataset in enumerate(data["results"], start=1):
    print(f"\n{index}. {dataset['title']}")
    print("Publisher:", dataset.get("publisher"))
    print("Identifier:", dataset.get("identifier"))
