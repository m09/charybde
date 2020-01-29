from pathlib import Path

from pytest import fixture

from charybde.parsers.fr_parser import FrParser


@fixture(scope="module")
def small_fr_dataset_path() -> str:
    return str(Path(__file__).parent / "small_fr_dump.xml.bz2")


def test_fr_parser_dump(small_fr_dataset_path: str) -> None:
    fr_parser = FrParser()
    results = set(fr_parser.parse(small_fr_dataset_path, tuple()))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) in results

    results = set(fr_parser.parse(small_fr_dataset_path, ("fr",)))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) not in results

    results = set(fr_parser.parse(small_fr_dataset_path, ("fr", "fro")))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) in results
