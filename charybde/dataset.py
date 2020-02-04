"""Create a dataset from a wiktionary dump."""

from bz2 import BZ2File
from collections import Counter, defaultdict
from logging import getLogger
from pathlib import Path
from re import match as re_match
from typing import Counter as Counter_type, Iterable, Iterator, Mapping, Optional, Tuple

from tqdm import tqdm

from charybde.parsers.parser import get_parser


_logger = getLogger(__name__)


def _language_code(path: Path) -> str:
    match = re_match(r"^(.+)wiktionary-.*$", path.name)
    if match is None:
        raise ValueError("Could not detect the language of the dump %s" % path)
    return match.group(1)


def parse_dumps(
    dump_paths: Iterable[Path], langs: Optional[Tuple[str, ...]] = ()
) -> Iterator[Tuple[str, str, str, int]]:
    """
    Return the words and the number of syllables found in the given wiktionary dumps.

    :param dump_paths: Iterable of paths to the wiktionary dumps.
    :param langs: Tuple of langs to consider. Empty tuple = consider all langs.
    :return: Iterable of tuples comprised of a word, its lang and its syllable count.
    """
    for dump_path in dump_paths:
        language_code = _language_code(dump_path)
        try:
            parser = get_parser(language_code)()
        except KeyError:
            _logger.warning(
                "Could not find a parser class for language code %s", language_code
            )
            raise
        yield from parser.parse(dump_path, langs)


def create_csv_dataset_from_dump(
    dumps_folder_path: str,
    output_path: str,
    langs: Optional[Tuple[str, ...]],
    dumps: Optional[Tuple[str, ...]],
) -> None:
    """
    Create a bz2-compressed TSV file of a dataset created from several wiktionaries.

    :param dumps_folder_path: Path to the wiktionary dumps folder.
    :param output_path: Path to the output compressed TSV file. Extension will be added.
    :param langs: Tuple of langs to consider. Empty tuple = consider all langs.
    """

    Counts = Mapping[str, Mapping[str, Mapping[str, Counter_type[int]]]]
    counts: Counts = defaultdict(lambda: defaultdict(lambda: defaultdict(Counter)))
    dump_paths = [
        p
        for p in Path(dumps_folder_path).iterdir()
        if p.is_file()
        and p.name.endswith(".xml.bz2")
        and (dumps is None or _language_code(p) in dumps)
    ]
    for word, pronounciation, lang, count in parse_dumps(dump_paths):
        counts[lang][word][pronounciation][count] += 1

    with BZ2File(output_path + ".tsv.bz2", "w") as fh:
        for lang, lang_stats in tqdm(counts.items()):
            for word, word_stats in lang_stats.items():
                for pronounciation, pronounciation_stats in word_stats.items():
                    count = pronounciation_stats.most_common(n=1)[0][0]
                    fh.write(
                        (
                            "%s\t%s\t%s\t%d\n" % (word, pronounciation, lang, count)
                        ).encode("utf-8")
                    )
