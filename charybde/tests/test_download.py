from pathlib import Path

from pytest import fixture

from charybde.download import Downloader


@fixture
def downloader() -> Downloader:
    return Downloader(
        str(Path(__file__).parent),
        mirror="https://web.archive.org"
        "/web/20180927140006/https://dumps.wikimedia.org/",
    )


def test_find_wiktionaries_folders(downloader: Downloader) -> None:
    results = set(downloader.find_wiktionaries_folders())
    assert len(results) > 50
    assert "enwiktionary" in (folder.split("/")[0] for folder in results)


def test_download_from_wiktionary_dump_folder(downloader: Downloader) -> None:
    folder = "mhwiktionary/20180920"
    downloader.download_from_wiktionary_dump_folder(folder)
