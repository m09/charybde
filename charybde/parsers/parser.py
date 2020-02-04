from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, Optional, Tuple, Type

from tqdm import tqdm
from tqdm.std import tqdm as TqdmType

from charybde.utils import import_submodules


class Parser:
    def parse(
        self, dump_path: Path, langs: Optional[Tuple[str, ...]]
    ) -> Iterator[Tuple[str, str, str, int]]:
        raise NotImplementedError()

    def _compute_counts(self, pronounciation: str) -> int:
        """
        Return the number of syllables of a word.

        :param pronounciation: The IPA pronounciation of the word.
        :return: The number of syllables in a word.
        """
        return pronounciation.count(" ") + pronounciation.count(".") + 1

    def _create_progress_bar(
        self, iterable: Iterable, language: str, unit: str = "lines"
    ) -> TqdmType:
        return tqdm(
            iterable,
            desc="Processing %s wiktionary" % language,
            unit=unit,
            unit_scale=True,
        )


_parsers: Dict[str, Type[Parser]] = {}


def register_parser(language_code: str) -> Callable[[Type[Parser]], Type[Parser]]:
    def wrapper(parser: Type[Parser]) -> Type[Parser]:
        _parsers[language_code] = parser
        return parser

    return wrapper


def get_parser(language_code: str) -> Type[Parser]:
    return _parsers[language_code]


import_submodules(".".join(__name__.split(".")[:-2]))
