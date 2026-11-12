
import requests
import json

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

response.raise_for_status()

data = response.json()

# 1. API jogabynyň esasy meýdanlary
print("API RESPONSE KEYS:")
print(list(data.keys()))

# 2. Birinji dataset-iň ähli meýdanlary
first_dataset = data["results"][0]

print("\nFIRST DATASET KEYS:")
print(list(first_dataset.keys()))

# 3. Birinji dataset-iň doly maglumatlary
print("\nFULL DATASET INFORMATION:")
print(json.dumps(
    first_dataset,
    indent=4,
    ensure_ascii=False
))

# 4. Ähli netijeleri JSON faýlyna ýazmak
with open("data/datasets.json", "w", encoding="utf-8") as file:
    json.dump(
        data["results"],
        file,
        indent=4,
        ensure_ascii=False
    )

print("\nData saved successfully!")