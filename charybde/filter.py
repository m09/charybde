from bz2 import BZ2File
from re import split


def filter_dataset(dataset_path: str, filtered_dataset_path: str) -> None:
    with_syllables = 0
    without = 0
    syllables = set()
    with BZ2File(dataset_path) as fh:
        for bytes_line in fh:
            line = bytes_line.decode("utf8")
            fields = line.strip().split("\t")
            try:
                word, pronounciation, lang, count = fields
            except ValueError:
                print(line)
            # print(word, pronounciation, lang, count)
            if "." in pronounciation:
                with_syllables += 1
                syllables.update(split("[. ]", pronounciation))
            else:
                without += 1
    print(with_syllables, without, syllables)
