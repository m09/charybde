from pathlib import Path
from typing import Callable, Dict, Iterable, Iterator, Optional, Tuple, Type, TypeVar

from tqdm import tqdm
from tqdm.std import tqdm as TqdmType

from charybde.utils import import_submodules


class Parser:
    def parse(
        self, dump_path: Path, langs: Optional[Tuple[str, ...]]
    ) -> Iterator[Tuple[str, str, str, int]]:
        """
        Parse a dump.

        Args:
            dump_path: Path to the dump to parse.
            langs: Limit the parsing to the matching langs.

        Returns:
            Iterable of tuples comprised of a word, its pronounciation (IPA), its lang \
                and its count.
        """
        raise NotImplementedError()

    def _compute_counts(self, pronounciation: str) -> int:
        """
        Count the number of syllables of a word.

        Args:
            pronounciation: The IPA pronounciation of the word.

        Returns:
            The number of syllables in a word.
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


_ParserT = TypeVar("_ParserT", bound=Parser)


def register_parser(language_code: str) -> Callable[[Type[_ParserT]], Type[_ParserT]]:
    """
    Create a decorator that declares a parser as able to parse the given lang.

    Args:
        language_code: The language code that the parser can handle.

    Returns:
        The decorator.
    """

    def decorator(parser: Type[_ParserT]) -> Type[_ParserT]:
        _parsers[language_code] = parser
        return parser

    return decorator


def get_parser(language_code: str) -> Type[Parser]:
    return _parsers[language_code]


import_submodules(".".join(__name__.split(".")[:-2]))
