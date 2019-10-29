from pathlib import Path

from pytest import fixture

from charybde.dataset import parse_dump


@fixture(scope="module")
def small_dataset_path() -> str:
    return str(Path(__file__).parent / "small_dump.xml.bz2")


def test_parse_dump(small_dataset_path: str) -> None:
    results = set(parse_dump(small_dataset_path, tuple()))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) in results

    results = set(parse_dump(small_dataset_path, ("fr",)))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) not in results

    results = set(parse_dump(small_dataset_path, ("fr", "fro")))
    assert ("accueil", "a.kœj", "fr", 2) in results
    assert ("lire", "liʁ", "fr", 1) in results
    assert ("lire", "liʁ", "fro", 1) in results
