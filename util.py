import itertools
from typing import Iterable, TypeVar

T = TypeVar("T")

def chunked_iterable(iterable: Iterable[T], size: int) -> Iterable[tuple[T, ...]]:
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, size))
        if not chunk:
            break
        yield chunk
