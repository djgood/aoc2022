from __future__ import annotations
from dataclasses import dataclass
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

@dataclass(frozen=True, eq=True)
class Point2D:
    x: int
    y: int

    def __sub__(self, other) -> Point2D:
        return Point2D(self.x - other.x, self.y - other.y)

    def manhattan(self: Point2D, other: Point2D) -> int:
        diff = self - other
        return abs(diff.x) + abs(diff.y)
