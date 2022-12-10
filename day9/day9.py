from __future__ import annotations
from dataclasses import dataclass
from typing import Set

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

@dataclass()
class RopeSegment:
    pos: Position = Position(0,0)

# Position is also used to show a diff of direction
input_mapping = {
    "U": Position(0, 1),
    "D": Position(0, -1),
    "L": Position(-1, 0),
    "R": Position(1, 0)
}

# not super proud of this
# depending on the diff, make the correct move to follow
diff_moves = {
    # basic
    Position(0, -2): Position(0, 1), # up
    Position(0, 2): Position(0, -1), # down
    Position(2, 0): Position(-1, 0), # left
    Position(-2, 0): Position(1, 0), # right

    # diag
    Position(-1, -2): Position(1, 1), # up-right
    Position(-2, -1): Position(1, 1),

    Position(1, -2): Position(-1, 1), # up-left
    Position(2, -1): Position(-1, 1),

    Position(-1, 2): Position(1, -1), # down-right
    Position(-2, 1): Position(1, -1),

    Position(2, 1): Position(-1, -1), # down-left
    Position(1, 2): Position(-1, -1),

    Position(-2, -2): Position(1, 1),
    Position(-2, 2): Position(1, -1),
    Position(2, -2): Position(-1, 1),
    Position(2, 2): Position(-1, -1),
}

class Rope:
    def __init__(self, length: int) -> None:
        self.rope_segments = []
        self.tail_visited: Set[Position] = set()
        self.tail_visited.add(Position(0,0))

        for _ in range(length):
            self.rope_segments.append(RopeSegment())

    def move_head(self, direction: Position):
        self.rope_segments[0].pos += direction
        # all elements after head
        for index in range(1, len(self.rope_segments)):
            diff = self.rope_segments[index].pos - self.rope_segments[index - 1].pos

            if diff in diff_moves:
                self.rope_segments[index].pos += diff_moves[diff]
            else:
                if abs(diff).x >= 2 or abs(diff).y >= 2:
                    raise Exception(f"Rope broke: {diff}")

                # no need to move, so the rest of the rope shouldn't 
                break


        self.tail_visited.add(self.rope_segments[-1].pos)

    def print_rope(self, grid_size: int):
        lines = []
        for y in range(grid_size, -(grid_size + 1), -1):
            line = ""
            for x in range(-grid_size - 20, grid_size + 21, 1):
                rope = None
                for index, seg in enumerate(self.rope_segments):
                    if seg.pos.x == x and seg.pos.y == y:
                        rope = index
                        break

                if rope is not None:
                    if rope == 0:
                        line += "H"
                    elif rope == len(self.rope_segments) - 1:
                        line += "T"
                    else:
                        line += str(rope)
                else:
                    if x == 0 and y == 0:
                        line += "s"
                    else:
                        pos = Position(x, y)
                        if pos in self.tail_visited:
                            line += "#"
                        else:
                            line += "."

            lines.append(line)
        print("\n".join(lines))

def main():
    rope = Rope(2)
    for instruction in read_input("input.txt"):
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            rope.move_head(input_mapping[direction])

    print("part1", len(rope.tail_visited))

    rope = Rope(10)
    for instruction in read_input("input.txt"):
        direction, count = instruction.split(" ")
        for _ in range(int(count)):
            rope.move_head(input_mapping[direction])

    print("part2", len(rope.tail_visited))

if __name__ == "__main__":
    main()
