"""Wiktionaries downloader."""

from hashlib import sha1
from os import makedirs
from os.path import join
from pathlib import Path
from shutil import rmtree
from typing import Iterator

from bs4 import BeautifulSoup
from requests import RequestException, get
from tqdm import tqdm


class Downloader:
    """Wiktionaries downloader."""

    def __init__(
        self, output_dir: str, mirror: str = "https://dumps.wikimedia.org"
    ) -> None:
        """
        Construct a wiktionaries downloader.

        Args:
            output_dir: Path to the folder where the wiktionaries will be downloaded.
            mirror: Wikimedia mirror to use.
        """
        self.output_dir = output_dir
        self.mirror = mirror
        self.headers = {"User-Agent": "Charybde (+https://github.com/m09/charybde/)"}
        makedirs(output_dir, exist_ok=True)

    def download_from_wiktionary_dump_folder(self, url: str) -> None:
        """
        Download a wiktionary dump from a wiktionary dump folder url.

        Args:
            url: URL pointing to the wiktionary dump folder.
        """
        response = get(f"{self.mirror}/{url}/dumpstatus.json", headers=self.headers)
        response.raise_for_status()
        json = response.json()
        files = json["jobs"]["metacurrentdump"]["files"]
        for filename, filestats in files.items():
            url, size, sha1 = filestats["url"], filestats["size"], filestats["sha1"]
            output_path = join(self.output_dir, filename)
            if Path(output_path).is_file() and self._sha1sum(output_path) == sha1:
                continue
            with open(output_path, "wb") as fh, self._create_pbar(
                filename, size
            ) as pbar:
                with get(
                    f"{self.mirror}/{url}", stream=True, headers=self.headers
                ) as response:
                    for chunk in response.iter_content(chunk_size=1024):
                        if chunk:
                            chunk_size = fh.write(chunk)
                            pbar.update(chunk_size)
            if self._sha1sum(output_path) != sha1:
                rmtree(output_path)
                raise RequestException()

    def find_wiktionaries_folders(self) -> Iterator[str]:
        """
        Find all available wiktionary dump folders from the Wikimedia dumps site.

        Returns:
            Iterator of URL pointing to wiktionary dump folders.
        """
        response = get(f"{self.mirror}/backup-index.html", headers=self.headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        for li in soup.find_all("li"):
            if li.find("span", class_="done"):
                a = li.find("a")
                if a and a.get_text().endswith("wiktionary"):
                    yield a.attrs["href"]

    def download_all_wiktionaries(self) -> None:
        """Download all current wiktionaries."""
        for folder in self.find_wiktionaries_folders():
            try:
                self.download_from_wiktionary_dump_folder(folder)
            except RequestException:
                print(f"Warning: folder {folder} could not be downloaded.")

    @staticmethod
    def _sha1sum(filename: str) -> str:
        """
        Compute the SHA1 digest of a file.

        Args:
            filename: Path to the file to hash.

        Returns:
            The SHA1 hash of the file.
        """
        hash = sha1()
        with open(filename, "rb") as fh:
            for chunk in iter(lambda: fh.read(128 * 1024), b""):
                hash.update(chunk)
        return hash.hexdigest()

    @staticmethod
    def _create_pbar(name: str, size: int) -> tqdm:
        """
        Create a tqdm progress bar to display download progress.

        Args:
            name: Name of the file being downloaded.
            size: Size of the file being downloaded.

        Returns:
            Progress bar.
        """
        return tqdm(total=size, desc=name, unit="o", unit_scale=True)
