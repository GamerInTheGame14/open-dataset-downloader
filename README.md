# Open Dataset Downloader

A Python command-line application for searching, downloading, and analyzing publicly available datasets using the Data.gov API.

Built as a portfolio project demonstrating API integration, file downloading, data processing, automated testing, and continuous integration.

## Features

- Search datasets using keywords
- Browse dataset titles, publishers, and descriptions
- Select datasets interactively
- Discover available download formats
- Download CSV, PDF, JSON, ZIP, and other supported file types
- Automatically assign file extensions based on MIME types
- Display download progress with `tqdm`
- Save selected dataset metadata as JSON
- Use temporary files to prevent incomplete downloads from being saved as completed files
- Analyze CSV datasets using pandas
- Run automated tests with pytest
- Run tests automatically using GitHub Actions

## Technologies

- Python 3.11
- Requests
- Pandas
- tqdm
- pytest
- GitHub Actions
- Data.gov API

## Installation

Clone the repository:

```bash
git clone https://github.com/GamerInTheGame14/open-dataset-downloader.git
cd open-dataset-downloader
```

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

Run the interactive downloader:

```bash
python src/search_cli.py
```

Example workflow:

```text
OPEN DATASET DOWNLOADER

Enter search keyword: population

Searching datasets...

[1] HHS Office of Minority Health Population Profiles
[2] Metadata for High Population Areas
...

Select dataset number (0 to cancel): 2

Available download formats:
[1] application/pdf

Select download format: 1

Downloading dataset...
metadata-for-high-population-areas.pdf: 100%

Download completed!
Filename: metadata-for-high-population-areas.pdf
Size: 160,749 bytes
```

Downloaded files and metadata are stored in the `data/` directory, which is excluded from version control.

## CSV Analysis

The project also includes a CSV analysis script demonstrating how to calculate:

- Total rows and columns
- Missing values by column
- Data completeness
- Duplicate rows
- Empty columns

The current analysis script uses a configured local CSV path. It is not yet integrated into the interactive downloader.

## Automated Tests

Install development dependencies:

```bash
pip install -r requirements-dev.txt
```

Run tests:

```bash
python -m pytest -v
```

Tests currently cover download format discovery and cleanup of incomplete downloads after a connection failure.

## Continuous Integration

GitHub Actions runs the automated tests on pushes and pull requests.

Workflow configuration: `.github/workflows/tests.yml`

## Limitations

- Dataset availability and supported formats depend on the source publisher.
- A downloadable dataset does not necessarily provide a CSV file.
- The downloader relies on MIME type metadata, which may occasionally be incomplete or inaccurate.
- API requests may be subject to rate limits.
- The CSV analysis script currently requires a locally configured file path.

## Project Status

Functional portfolio demonstration with an interactive downloader, basic CSV analysis, automated tests, and GitHub Actions CI.

## Author

GamerInTheGame14

_Independent portfolio project — not commissioned client work._
