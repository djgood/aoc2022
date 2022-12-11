from io import TextIOWrapper
from typing import List
from functools import reduce
import operator

from result import Result

def parse_input(file: TextIOWrapper):
    for line in file:
        yield line.strip()

def tallest_tree(line: list[int]) -> bool:
    """check if first element is tallest"""
    this_tree = line[0]
    for tree in line[1:]:
        if tree >= this_tree:
            return False

    return True

def distance_to_blocking(line: list[int]) -> int:
    this_tree = line[0]
    for count, tree in enumerate(line[1:]):
        if tree >= this_tree:
            return count + 1

    return len(line) - 1

def generate_sightlines(trees: List[List[int]], x: int, y: int):
    max_coord = len(trees)
    s1, s2, s3, s4 = [], [], [], []
    for x_cur in range(x, max_coord, 1):
        s1.append(trees[y][x_cur])

    for x_cur in range(x, -1, -1):
        s2.append(trees[y][x_cur])

    for y_cur in range(y, max_coord, 1):
        s3.append(trees[y_cur][x])

    for y_cur in range(y, -1, -1):
        s4.append(trees[y_cur][x])

    return s1, s2, s3, s4

def is_visible(trees: List[List[int]], x: int, y: int) -> int:
    sightlines = []
    sightlines += generate_sightlines(trees, x, y)

    for s in sightlines:
        if tallest_tree(s):
            return 1

    return 0

def senic_score(trees: List[List[int]], x: int, y: int) -> int:
    sightlines = []
    sightlines += generate_sightlines(trees, x, y)

    senic_scores = []
    for s in sightlines:
        senic_scores.append(distance_to_blocking(s))

    return reduce(operator.mul, senic_scores, 1)

def main(input_file: TextIOWrapper) -> Result:
    trees = []
    # load file as 2d array
    for line in parse_input(input_file):
        trees.append([int(x) for x in list(line)])

    assert len(trees) == len(trees[0])
    visible = 0
    max_coord = len(trees)
    max_ss = 0
    for y in range(max_coord):
        for x in range(max_coord):

            if x in [0, max_coord - 1] or y in [0, max_coord - 1]:
                # edge is visible
                visible += 1
            else:
                # interior
                if is_visible(trees, x, y):
                    visible += 1

                ss = senic_score(trees, x, y)
                max_ss = max(max_ss, ss)

    return Result(visible, max_ss)
