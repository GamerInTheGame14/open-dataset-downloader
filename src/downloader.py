
import json
import requests

from pathlib import Path


# Project directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_FILE = DATA_DIR / "datasets.json"

DATA_DIR.mkdir(exist_ok=True)


def load_datasets():
    """Load datasets from previously saved JSON file."""

    with open(DATA_FILE, "r", encoding="utf-8") as file:
        return json.load(file)


def get_csv_download_url(dataset):
    """Find CSV download URL inside dataset distributions."""

    distributions = dataset.get("dcat", {}).get(
        "distribution", []
    )

    for item in distributions:
        media_type = item.get("mediaType", "").lower()

        if media_type == "text/csv":
            return item.get("downloadURL")

    return None


def download_dataset(url, filename):
    """Download dataset and save it locally."""

    output_path = DATA_DIR / filename

    print(f"Downloading: {filename}")

    response = requests.get(
        url,
        stream=True,
        timeout=60
    )

    response.raise_for_status()

    total_size = 0

    with open(output_path, "wb") as file:
        for chunk in response.iter_content(chunk_size=8192):

            if chunk:
                file.write(chunk)
                total_size += len(chunk)

    print("\nDownload completed!")
    print(f"File: {output_path}")
    print(f"Size: {total_size:,} bytes")

    return output_path


def main():

    datasets = load_datasets()

    # Select first dataset
    dataset = datasets[0]

    print("Dataset:", dataset["title"])

    download_url = get_csv_download_url(dataset)

    if not download_url:
        print("CSV download URL not found!")
        return

    filename = dataset.get("slug", "dataset") + ".csv"

    download_dataset(download_url, filename)


if __name__ == "__main__":
    main()
