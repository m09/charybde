from pathlib import Path
from re import compile as re_compile
from typing import Iterator, Optional, Tuple

from charybde.parsers.dump_parser import parse
from charybde.parsers.parser import Parser, register_parser


@register_parser(language_code="en")
class EnParser(Parser):
    def parse(
        self, dump_path: Path, langs: Optional[Tuple[str, ...]]
    ) -> Iterator[Tuple[str, str, str, int]]:

        pattern = re_compile(r"{{IPA\|([^|]+?)\|/(.+?)/.*?}}")

        for page in self._create_progress_bar(parse(dump_path), "English", "pages"):
            word = page["title"]
            match = pattern.search(page["revision"]["text"]["#text"])
            if match:
                lang, pronounciation = match.groups()
                yield word, pronounciation, lang, self._compute_counts(pronounciation)
