from __future__ import annotations
from dataclasses import dataclass
from typing import Dict, Tuple

def read_input(file):
    with open(file) as file:
        for line in file:
            yield line.strip()

@dataclass(eq=True, frozen=True)
class Position:
    x: int
    y: int

    def __add__(self, other: Position) -> Position:
        return Position(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Position) -> Position:
        return Position(self.x - other.x, self.y - other.y)

    def __abs__(self) -> Position:
        return Position(abs(self.x), abs(self.y))

class BasicRope:
    def __init__(self) -> None:
        self.tail_visited: Dict[Position, bool] = dict()
        self.head: Position = Position(0, 0)
        self.tail: Position = Position(0, 0)
        self._tail_visit(self.tail)

    def _tail_visit(self, pos: Position):
        self.tail_visited[pos] = True

    def move_head(self, d: Position, count: int):
        for _ in range(count):
            new_head = self.head + d
            diff = abs(new_head - self.tail)
            if diff.x >= 2 or diff.y >= 2:
                # rope follows last position of head
                self.tail = self.head
            else:
                # rope stays
                pass

            self.head = new_head
            self._tail_visit(self.tail)

input_mapping = {
    "U": Position(0, 1),
    "D": Position(0, -1),
    "L": Position(-1, 0),
    "R": Position(1, 0)
}

def main():
    rope = BasicRope()
    for instruction in read_input("sample_input.txt"):
        direction, count = instruction.split(" ")
        rope.move_head(input_mapping[direction], int(count))

    print(len(rope.tail_visited.values()))

if __name__ == "__main__":
    main()
