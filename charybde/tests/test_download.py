from pathlib import Path
from unittest import main, TestCase

from charybde.download import Downloader


tests_dir = str(Path(__file__).parent)


class DownloadTests(TestCase):

    def setUp(self):
        self.downloader = Downloader(tests_dir)

    def test_find_wiktionaries_folders(self):
        results = set(self.downloader.find_wiktionaries_folders())
        self.assertGreater(len(results), 50)
        self.assertIn("enwiktionary", (folder.split("/")[0] for folder in results))

    def test_download_from_wiktionary_dump_folder(self):
        folder = "mhwiktionary/20180920"
        self.downloader.download_from_wiktionary_dump_folder(folder)


if __name__ == "__main__":
    main()
