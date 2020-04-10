from tempfile import TemporaryDirectory
from typing import Iterator

from pytest import fixture
from pytest import mark

from charybde.download import Downloader


@fixture(scope="module")
def downloader() -> Iterator[Downloader]:
    with TemporaryDirectory(prefix="charybde-") as temp_dir:
        yield Downloader(
            temp_dir,
            mirror="https://web.archive.org"
            "/web/20180927140006id_/https://dumps.wikimedia.org",
        )


@mark.skip("Cannot query webarchive with requests, Client Error.")
def test_find_wiktionaries_folders(downloader: Downloader) -> None:
    results = set(downloader.find_wiktionaries_folders())
    print(results)
    assert len(results) > 50
    assert "enwiktionary" in (folder.split("/")[0] for folder in results)


@mark.skip("Cannot query webarchive with requests, Client Error.")
def test_download_from_wiktionary_dump_folder(downloader: Downloader) -> None:
    folder = "mhwiktionary/20180920"
    downloader.download_from_wiktionary_dump_folder(folder)
