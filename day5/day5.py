from copy import deepcopy
from io import TextIOWrapper
import re
from typing import Tuple

from result import Result

class Stack:

    def __init__(self, crates: list[str]):
        self.crates: list[str] = crates

    def __repr__(self) -> str:
        r = ""
        for crate in self.crates:
            r += f"[{crate}] "

        return r

    def add_crate(self, crate: str) -> None:
        assert len(crate) == 1
        self.crates.append(crate)

    def pop_crate(self) -> str:
        return self.crates.pop()

class Supplies:

    def __init__(self, num_stacks: int) -> None:
        self.stacks: list[Stack] = []
        for _ in range(num_stacks):
            self.stacks.append(Stack([]))

    def __repr__(self) -> str:
        r = ""
        for num, stack in enumerate(self.stacks):
            r += f"{num + 1} {stack}\n"

        return r

    def move(self, raw_num: str, raw_from_stack: str, raw_to_stack: str) -> None:
        num = int(raw_num)
        from_stack = int(raw_from_stack) - 1
        to_stack = int(raw_to_stack) - 1

        for _ in range(num):
            self.stacks[to_stack].add_crate(self.stacks[from_stack].pop_crate())

    def move_in_order(self, raw_num: str, raw_from_stack: str, raw_to_stack: str) -> None:
        num = int(raw_num)
        from_stack = int(raw_from_stack) - 1
        to_stack = int(raw_to_stack) - 1

        crates = []
        for _ in range(num):
            crates.insert(0, self.stacks[from_stack].pop_crate())

        for crate in crates:
            self.stacks[to_stack].add_crate(crate)


def parse_input(file: TextIOWrapper) -> Tuple[list[str], list[str]]:
    drawing: list[str] = []
    steps: list[str] = []
    drawing_over = False
    for line in file:
        if line == "\n":
            drawing_over = True
            continue

        if not drawing_over:
            drawing.append(line)
        else:
            steps.append(line)

    return drawing, steps


def main(input_file: TextIOWrapper) -> Result:
    drawing, steps = parse_input(input_file)
    drawing.reverse()
    num_stacks = len(drawing.pop(0).strip().split("   "))

    s = Supplies(num_stacks)

    for line in drawing:
        for stack in range(num_stacks):
            cursor = 4*stack
            crate = line[cursor:cursor+4].strip()
            if crate != "":
                s.stacks[stack].add_crate(crate[1])

    s2 = deepcopy(s)

    move_regex = re.compile("^move (\\d+) from (\\d+) to (\\d+)$")
    for step in steps:
        result = move_regex.match(step.strip())
        assert result is not None
        s.move(result.group(1), result.group(2), result.group(3))
        s2.move_in_order(result.group(1), result.group(2), result.group(3))

    output = ""
    for stack in s.stacks:
        output += stack.pop_crate()

    output1 = output

    output = ""
    for stack in s2.stacks:
        output += stack.pop_crate()

    output2 = output
    return Result(output1, output2)

