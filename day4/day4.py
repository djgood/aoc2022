
from __future__ import annotations
from dataclasses import dataclass
from typing import Iterator


class Range:
    """ Represents a range of numbers (closed-set)"""

    def __init__(self, start: int, end: int):
        self.start = start
        self.end = end

    def __repr__(self) -> str:
        return f"{self.start}-{self.end}"

    @staticmethod
    def from_string(string: str) -> Range:
        nums = string.split("-")
        return Range(int(nums[0]), int(nums[1]))

    def contains(self, other: Range) -> bool:
        """Is this set contained within the other?"""
        return (self.start >= other.start) and (self.end <= other.end)

    def overlaps(self, other: Range) -> bool:
        """Is there any overlap at all with the other?"""
        return (self.end >= other.start) and (other.end >= self.start)

@dataclass
class RangePair:
    range1: Range
    range2: Range

def read_input(filename) -> Iterator[RangePair]:
    with open(filename) as file:
        for line in file:
            ranges = line.strip().split(",")
            range1 = Range.from_string(ranges[0])
            range2 = Range.from_string(ranges[1])
            yield RangePair(range1, range2)

def main():
    contains = 0
    overlaps = 0
    for rp in read_input("input.txt"):
        if rp.range1.contains(rp.range2) or rp.range2.contains(rp.range1):
            contains += 1

        if rp.range1.overlaps(rp.range2):
            overlaps += 1

    print(contains)
    print(overlaps)

if __name__ == "__main__":
    main()
