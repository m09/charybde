from pathlib import Path
from unittest import main, TestCase

from charybde.dataset import parse_dump


class DatasetTests(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.small_dataset_path = str(Path(__file__).parent / "small_dump.xml.bz2")

    def test_parse_dump(self):
        results = set(parse_dump(self.small_dataset_path, tuple()))
        self.assertIn(("accueil", "fr", 2), results)
        self.assertIn(("lire", "fr", 1), results)
        self.assertIn(("lire", "fro", 1), results)

        results = set(parse_dump(self.small_dataset_path, ("fr",)))
        self.assertIn(("accueil", "fr", 2), results)
        self.assertIn(("lire", "fr", 1), results)
        self.assertNotIn(("lire", "fro", 1), results)

        results = set(parse_dump(self.small_dataset_path, ("fr", "fro")))
        self.assertIn(("accueil", "fr", 2), results)
        self.assertIn(("lire", "fr", 1), results)
        self.assertIn(("lire", "fro", 1), results)


if __name__ == "__main__":
    main()
