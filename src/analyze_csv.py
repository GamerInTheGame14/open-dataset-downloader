
import json
import pandas as pd

from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"

CSV_FILE = DATA_DIR / (
    "nyc-climate-budgeting-report-climate-alignment-assessment-and-capital-climate-investments.csv"
)

REPORT_FILE = DATA_DIR / "analysis_report.json"

CHUNK_SIZE = 100_000


def analyze_csv(file_path):

    print("Starting CSV analysis...\n")

    file_path = Path(file_path)

    # Read preview
    preview = pd.read_csv(
        file_path,
        nrows=5,
        dtype="string"
    )

    columns = preview.columns.tolist()

    print("COLUMNS:")
    for column in columns:
        print("-", column)

    print("\nPREVIEW:")
    print(preview.to_string(index=False))

    # Statistics
    total_rows = 0
    missing_values = {column: 0 for column in columns}
    data_types = {}
    unique_row_hashes = set()

    print("\nAnalyzing dataset in chunks...")

    for chunk in pd.read_csv(
        file_path,
        chunksize=CHUNK_SIZE,
        dtype="string"
    ):

        total_rows += len(chunk)

        # Missing values
        chunk_missing = chunk.isna().sum()

        for column in columns:
            missing_values[column] += int(
                chunk_missing[column]
            )

        # Data types
        for column, dtype in chunk.dtypes.items():
            data_types[column] = str(dtype)

        # Duplicate rows across all chunks
        hashes = pd.util.hash_pandas_object(
            chunk,
            index=False
        )

        unique_row_hashes.update(hashes.tolist())

        print(f"Processed: {total_rows:,} rows")

    # Duplicate statistics
    duplicate_rows = total_rows - len(unique_row_hashes)

    total_cells = total_rows * len(columns)

    missing_cells = sum(missing_values.values())

    completeness = (
        (total_cells - missing_cells) / total_cells * 100
        if total_cells else 0
    )

    # Column statistics
    column_statistics = {}

    for column in columns:

        missing_count = missing_values[column]

        missing_percentage = (
            missing_count / total_rows * 100
            if total_rows else 0
        )

        column_statistics[column] = {
            "data_type": data_types.get(column, "unknown"),
            "missing_values": missing_count,
            "missing_percentage": round(
                missing_percentage, 2
            )
        }

    # Empty columns
    empty_columns = [
        column
        for column, count in missing_values.items()
        if count == total_rows
    ]

    # Final report
    report = {
        "file_name": file_path.name,
        "file_size_bytes": file_path.stat().st_size,
        "total_rows": total_rows,
        "total_columns": len(columns),
        "total_missing_cells": missing_cells,
        "completeness_percentage": round(completeness, 2),
        "duplicate_rows": duplicate_rows,
        "empty_columns": empty_columns,
        "column_statistics": column_statistics
    }

    with open(REPORT_FILE, "w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False
        )

    # Display report
    print("\n" + "=" * 45)
    print("DATASET QUALITY REPORT")
    print("=" * 45)

    print(f"Total rows: {total_rows:,}")
    print(f"Total columns: {len(columns)}")
    print(f"File size: {file_path.stat().st_size:,} bytes")
    print(f"Missing cells: {missing_cells:,}")
    print(f"Completeness: {completeness:.2f}%")
    print(f"Duplicate rows: {duplicate_rows:,}")

    print("\nEmpty columns:")
    for column in empty_columns:
        print("-", column)

    print("\nColumn statistics:")

    for column, stats in column_statistics.items():
        print(
            f"{column}: "
            f"{stats['missing_percentage']}% missing"
        )

    print("\nReport saved:", REPORT_FILE)


if __name__ == "__main__":

    if CSV_FILE.exists():
        analyze_csv(CSV_FILE)
    else:
        print("CSV file not found!")
