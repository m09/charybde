from bz2 import BZ2File
from pathlib import Path
from queue import Queue
from threading import Thread
from typing import Any, Callable, Dict, Iterator, List, Tuple

from xmltodict import parse as xmltodict_parse


def parse(dump: Path) -> Iterator[Dict[str, Any]]:
    def filter(path: List[Tuple[str, Dict[str, str]]], item: Dict[str, Any]) -> bool:
        return (
            len(path) == 2
            and path[1][0] == "page"
            and item["ns"] == "0"
            and "redirect" not in item
        )

    queue: Queue = Queue()
    thread = Thread(target=_parse_dump, args=(dump, queue, filter))
    thread.start()
    while True:
        item = queue.get()
        if item is None:
            break
        yield item


def _parse_dump(
    dump: Path,
    output_queue: Queue,
    filter_callable: Callable[[List[Tuple[str, Dict[str, str]]], Dict[str, Any]], bool],
) -> None:
    def handler(path: List[Tuple[str, Dict[str, str]]], item: Dict[str, Any]) -> bool:
        if filter_callable(path, item):
            output_queue.put_nowait(item)
        return True

    with BZ2File(str(dump)) as fh:
        xmltodict_parse(fh, item_depth=2, item_callback=handler)
    output_queue.put(None)
