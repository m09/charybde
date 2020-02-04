from bz2 import BZ2File
from pathlib import Path
from re import compile as re_compile
from typing import Iterator, Optional, Tuple

from charybde.parsers.parser import Parser, register_parser


@register_parser(language_code="fr")
class FrParser(Parser):
    def parse(
        self, dump_path: Path, langs: Optional[Tuple[str, ...]]
    ) -> Iterator[Tuple[str, str, str, int]]:
        if langs:
            langs_joined = "|".join(langs)
        else:
            langs_joined = ".+?"
        pattern = re_compile(
            r"'''(.+?)''' \{\{pron\|(.+?)\|(?:lang=)?(%s)}}" % langs_joined
        )
        # en_pattern = {{IPA|en|/əˈkeɪ.di.n̩/|/əˈkeɪ.dʒn̩/}}
        with BZ2File(str(dump_path)) as fh:
            for line in self._create_progress_bar(fh, "French"):
                match = pattern.search(line.decode("utf-8", "replace"))
                if match:
                    word, pronounciation, lang = match.groups()
                    count = self._compute_counts(pronounciation)
                    yield word, pronounciation, lang, count
