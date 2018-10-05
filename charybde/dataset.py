"""Create a dataset from a wiktionary dump."""

from bz2 import BZ2File
from collections import Counter, defaultdict
from pathlib import Path
import re
from typing import Counter as Counter_type, Iterable, Mapping, Tuple

from tqdm import tqdm


def compute_counts(word: str, pronounciation: str, lang: str) -> int:
    """
    Return the number of syllables of a word.

    :param word: The word (sometimes multi-word like “Barbe à papa”) in question.
    :param pronounciation: The IPA pronounciation of the word.
    :param lang: The lang of the word.
    :return: The number of syllables in a word.
    """
    return pronounciation.count(" ") + pronounciation.count(".") + 1


def parse_dump(dump_path: str, langs: Tuple[str, ...] = ()) -> Iterable[Tuple[str, str, int]]:
    """
    Return the words and the number of syllables found in a wiktionary dump.

    :param dump_path: Path to the wiktionary dump.
    :param langs: Tuple of langs to consider. Empty tuple = consider all langs.
    :return: Iterable of tuples comprised of a word, its lang and its syllable count.
    """
    if langs:
        langs_joined = "|".join(langs)
    else:
        langs_joined = ".+?"
    pattern = re.compile(r"'''(.+?)''' \{\{pron\|(.+?)\|(?:lang=)?(%s)}}" % langs_joined)
    with BZ2File(dump_path) as fh:
        for line in fh:
            match = pattern.search(line.decode("utf-8", "replace"))
            if match:
                word, pronounciation, lang = match.groups()
                yield word, lang, compute_counts(word, pronounciation, lang)


def parse_dumps(dump_paths: Iterable[str], langs: Tuple[str, ...] = ()
                ) -> Iterable[Tuple[str, str, int]]:
    """
    Return the words and the number of syllables found in the given wiktionary dumps.

    :param dump_paths: Iterable of paths to the wiktionary dumps.
    :param langs: Tuple of langs to consider. Empty tuple = consider all langs.
    :return: Iterable of tuples comprised of a word, its lang and its syllable count.
    """
    for dump_path in dump_paths:
        yield from parse_dump(dump_path, langs)


def create_csv_dataset_from_dump(dumps_folder_path: str, output_path: str,
                                 langs: Tuple[str, ...] = ()) -> None:
    """
    Create a bz2-compressed TSV file of a dataset created from several wiktionaries.

    :param dumps_folder_path: Path to the wiktionary dumps folder.
    :param output_path: Path to the output compressed TSV file. Extension will be added.
    :param langs: Tuple of langs to consider. Empty tuple = consider all langs.
    """
    Counts = Mapping[str, Mapping[str, Counter_type[int]]]
    counts: Counts = defaultdict(lambda: defaultdict(Counter))
    for file in Path(dumps_folder_path).iterdir():
        if file.is_file() and file.name.endswith(".xml.bz2"):
            for word, lang, count in tqdm(parse_dump(str(file), langs=langs)):
                counts[lang][word][count] += 1
    with BZ2File(output_path + ".tsv.bz2", "w") as fh:
        for lang, lang_stats in tqdm(counts.items()):
            for word, word_stats in tqdm(lang_stats.items()):
                count = word_stats.most_common(n=1)[0][0]
                fh.write(("%s\t%s\t%d\n" % (word, lang, count)).encode("utf-8"))
