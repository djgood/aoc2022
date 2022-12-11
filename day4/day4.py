
from __future__ import annotations
from dataclasses import dataclass
from io import TextIOWrapper
from typing import Iterator

from result import Result

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

def parse_input(file: TextIOWrapper) -> Iterator[RangePair]:
    for line in file:
        ranges = line.strip().split(",")
        range1 = Range.from_string(ranges[0])
        range2 = Range.from_string(ranges[1])
        yield RangePair(range1, range2)

def main(input_file: TextIOWrapper) -> Result:
    contains = 0
    overlaps = 0
    for rp in parse_input(input_file):
        if rp.range1.contains(rp.range2) or rp.range2.contains(rp.range1):
            contains += 1

        if rp.range1.overlaps(rp.range2):
            overlaps += 1

    return Result(contains, overlaps)

