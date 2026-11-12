import sys
from pathlib import Path

sys.path.insert(
    0,
    str(Path(__file__).resolve().parent.parent / "src")
)

from search_cli import get_download_options


def test_get_download_options():
    dataset = {
        "dcat": {
            "distribution": [
                {
                    "mediaType": "application/pdf",
                    "downloadURL": "https://example.com/file.pdf"
                },
                {
                    "mediaType": "text/csv",
                    "downloadURL": "https://example.com/file.csv"
                },
                {
                    "mediaType": "application/json"
                }
            ]
        }
    }

    options = get_download_options(dataset)

    assert len(options) == 2
    assert options[0]["format"] == "application/pdf"
    assert options[1]["format"] == "text/csv"
    assert options[1]["url"] == "https://example.com/file.csv"



import requests
import pytest
import search_cli


def test_download_cleanup_on_error(tmp_path, monkeypatch):
    # Use a temporary directory instead of real data/.
    monkeypatch.setattr(search_cli, "DATA_DIR", tmp_path)

    class FakeResponse:
        headers = {"content-length": "100"}

        def raise_for_status(self):
            pass

        def iter_content(self, chunk_size):
            yield b"Hello"
            raise requests.ConnectionError("Connection lost")

    def fake_get(*args, **kwargs):
        return FakeResponse()

    monkeypatch.setattr(search_cli.requests, "get", fake_get)

    dataset = {"slug": "test-dataset"}

    with pytest.raises(requests.ConnectionError):
        search_cli.download_dataset(
            "https://example.com/test.csv",
            dataset,
            "text/csv"
        )

    assert not (tmp_path / "test-dataset.csv.part").exists()
    assert not (tmp_path / "test-dataset.csv").exists()
