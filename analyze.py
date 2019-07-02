from argparse import ArgumentParser
from bz2 import BZ2File
from collections import Counter
from typing import Counter as CounterType, Dict


def touches(input_dataset: str) -> None:
    touches: CounterType[str] = Counter()
    pronounciations: Dict[str, str] = {}
    with BZ2File(input_dataset, "r") as fh:
        for line in fh:
            word, pronounciation, lang, count = line.decode("utf-8").split("\t")
            if lang == "fr" and " " not in word:
                stripped = [c for c in pronounciation if c not in [" ", ".", "‿"]]
                n_touches = 0
                previous_c = None
                for c in stripped:
                    if c in ["m", "b", "p"] and previous_c not in ["m", "b", "p"]:
                        n_touches += 1
                    previous_c = c
                touches[word] = n_touches
                pronounciations[word] = pronounciation
    for word, n_touches in touches.most_common(1000):
        print(word, pronounciations[word], n_touches)


def b(input_dataset: str) -> None:
    with BZ2File(input_dataset, "r") as fh:
        for line in fh:
            word, pronounciation, lang, count = line.decode("utf-8").split("\t")
            if (
                lang == "fr"
                and " " not in word
                and "{" not in pronounciation
                and "}" not in pronounciation
                and "{" not in word
                and "}" not in word
            ):
                b_pronounciation = pronounciation.count("b")
                b_word = 0
                prev_char = None
                for char in word:
                    if char == "b" and prev_char != "b":
                        b_word += 1
                    prev_char = char
                total_pronounciation = pronounciation.count("p") + pronounciation.count(
                    "b"
                )
                total_word = word.count("p") + word.count("b")
                if total_pronounciation < total_word and b_pronounciation < b_word:
                    print("%40s %40s" % (word, pronounciation))


def main() -> None:
    parser = ArgumentParser("Inspect syllable datasets")
    subparsers = parser.add_subparsers(help="Commands")
    parser_touches = subparsers.add_parser("touches")
    parser_touches.set_defaults(handler=touches)
    parser_touches.add_argument(
        "input_dataset", help="Dataset to use for touches computations."
    )
    parser_b = subparsers.add_parser("b")
    parser_b.set_defaults(handler=b)
    parser_b.add_argument(
        "input_dataset", help="Dataset to use for mute b computations."
    )
    args = parser.parse_args()
    handler = args.handler
    delattr(args, "handler")
    handler(**vars(args))


if __name__ == "__main__":
    main()
