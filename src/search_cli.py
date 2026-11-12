import json
import re
import requests

from pathlib import Path
from tqdm import tqdm


API_URL = "https://api.gsa.gov/technology/datagov/v4/search"

API_KEY = "DEMO_KEY"

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

DATA_DIR.mkdir(exist_ok=True)


def search_datasets(keyword, limit=10):
    """Search datasets using Data.gov API."""

    headers = {
        "X-Api-Key": API_KEY
    }

    params = {
        "q": keyword,
        "per_page": limit
    }

    print("\nSearching datasets...")

    response = requests.get(
        API_URL,
        headers=headers,
        params=params,
        timeout=30
    )

    response.raise_for_status()

    return response.json().get("results", [])


def display_datasets(datasets):
    """Display search results."""

    print("\n" + "=" * 70)
    print("DATASET SEARCH RESULTS")
    print("=" * 70)

    for index, dataset in enumerate(datasets, start=1):

        print(f"\n[{index}] {dataset.get('title', 'Unknown')}")

        print("Publisher:", dataset.get("publisher", "Unknown"))

        print(
            "Download available:",
            "Yes" if dataset.get("has_download") else "No"
        )

        print(
            "Description:",
            (dataset.get("description") or "No description")[:200]
        )

        print("-" * 70)


def get_download_options(dataset):
    distributions = dataset.get("dcat", {}).get("distribution", [])

    options = []

    for item in distributions:
        url = item.get("downloadURL")

        if url:
            options.append({
                "format": item.get("mediaType", "Unknown"),
                "url": url
            })

    return options


def display_download_options(options):
    print("\nAvailable download formats:")

    for index, option in enumerate(options, start=1):
        print(f"[{index}] {option['format']}")




def download_dataset(url, dataset, media_type):
    slug = dataset.get("slug", "dataset")
    slug = re.sub(r"[^a-zA-Z0-9_-]", "-", slug)

    extensions = {
        "text/csv": ".csv",
        "application/pdf": ".pdf",
        "application/json": ".json",
        "application/zip": ".zip",
        "application/vnd.ms-excel": ".xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": ".xlsx",
        "text/xml": ".xml",
        "application/xml": ".xml",
    }

    extension = extensions.get(media_type.lower(), ".bin")
    filename = f"{slug}{extension}"
    output_path = DATA_DIR / filename

    print("\nDownloading dataset...")

    response = requests.get(url, stream=True, timeout=60)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))

    
    # Download into a temporary file first.
    temp_path = output_path.with_name(output_path.name + ".part")

    try:
        with open(temp_path, "wb") as file:
            with tqdm(
                total=total_size if total_size > 0 else None,
                unit="B",
                unit_scale=True,
                desc=filename
            ) as progress:

                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        progress.update(len(chunk))

        # Check whether download size matches server response.
        downloaded_size = temp_path.stat().st_size

        if total_size > 0 and downloaded_size != total_size:
            raise IOError("Incomplete download: file size mismatch")

        # Only publish the completed file.
        temp_path.replace(output_path)

    except (requests.RequestException, OSError):
        if temp_path.exists():
            temp_path.unlink()
        raise


    print("\nDownload completed!")
    print("Filename:", filename)
    print(f"Size: {output_path.stat().st_size:,} bytes")

    return output_path




def save_metadata(dataset):

    metadata_file = DATA_DIR / "selected_dataset.json"

    with open(
        metadata_file,
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            dataset,
            file,
            indent=4,
            ensure_ascii=False
        )

    print("Metadata saved:", metadata_file)


def main():

    print("=" * 70)
    print("OPEN DATASET DOWNLOADER")
    print("=" * 70)

    keyword = input("\nEnter search keyword: ").strip()

    if not keyword:
        print("Search keyword cannot be empty!")
        return

    try:
        datasets = search_datasets(keyword)

        if not datasets:
            print("No datasets found!")
            return

        display_datasets(datasets)

        choice = input(
            "\nSelect dataset number (0 to cancel): "
        ).strip()

        if not choice.isdigit():
            print("Invalid selection!")
            return

        selected_index = int(choice)

        if selected_index == 0:
            print("Download cancelled.")
            return

        if selected_index > len(datasets):
            print("Dataset number does not exist!")
            return

        dataset = datasets[selected_index - 1]

        save_metadata(dataset)

        options = get_download_options(dataset)

        if not options:
            print("\nNo downloadable files found for this dataset.")
            return

        display_download_options(options)

        choice = input("\nSelect download format: ").strip()

        if not choice.isdigit():
            print("Invalid selection!")
            return

        selected_index = int(choice)

        if selected_index < 1 or selected_index > len(options):
            print("Invalid format number!")
            return

        selected_option = options[selected_index - 1]

        download_dataset(
            selected_option["url"],
            dataset,
            selected_option["format"]
        )

    except requests.RequestException as error:
        print("\nAPI or download error:", error)

    except OSError as error:
        print("\nFile error:", error)


if __name__ == "__main__":
    main()
