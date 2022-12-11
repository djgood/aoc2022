import heapq
from io import TextIOWrapper

from result import Result

def main(input_file: TextIOWrapper):
    elves = []
    calories_buffer = 0
    for line in input_file:
        if line == "\n":
            heapq.heappush(elves, -calories_buffer)
            calories_buffer = 0
        else:
            calories_buffer += int(line)

    top3 = [-heapq.heappop(elves) for _ in range(3)]
    return Result(top3[0], sum(top3))

