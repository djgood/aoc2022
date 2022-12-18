from io import TextIOWrapper
import itertools
from typing import Iterator, List

from result import Result
from util import chunked_iterable

def parse_input(file: TextIOWrapper) -> Iterator[str]:
    for line in file:
        yield line.strip()

def priority(letter: str) -> int:
    char = ord(letter)
    if ord('a') <= char and char <= ord('z'):
        priority = char - 96

    elif ord('A') <= char and char <= ord('Z'):
        priority = char - 64 + 26
    else:
        raise Exception("pls help")

    return priority

class Priorities:
    part1: List[int] = []
    part2: List[int] = []

def main(input_file: TextIOWrapper) -> Result:
    priorities = Priorities()
    input1, input2 = itertools.tee(parse_input(input_file))

    for rucksack in input1:
        compartment_len = int(len(rucksack)/2)
        rucksack = (rucksack[0:compartment_len], rucksack[compartment_len:])
        rucksack = (set(rucksack[0]), set(rucksack[1]))
        same = rucksack[0].intersection(rucksack[1])
        priorities.part1.append(priority(same.pop()))

    for rucksacks in chunked_iterable(input2, 3):
        rucksacks_sets = [set(rucksack) for rucksack in rucksacks]
        same = rucksacks_sets[0].intersection(rucksacks_sets[1]).intersection(rucksacks_sets[2])
        priorities.part2.append(priority(same.pop()))

    return Result(sum(priorities.part1), sum(priorities.part2))

