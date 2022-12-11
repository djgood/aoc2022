from io import TextIOWrapper
from typing import Iterator

from result import Result

def input(file: TextIOWrapper) -> Iterator[str]:
    for line in file:
        yield line.strip()

def main(input_file: TextIOWrapper) -> Result:
    cycle = 0
    X = 1

    beam_col = 0
    beam_row = 0

    pipeline = []
    for line in input(input_file):
        pipeline.append(line)

    crt_lines = []
    crt_line = ""
    interesting_cycle = []
    while len(pipeline) > 0:
        # cycle begins
        instruction = pipeline.pop(0).split(" ")
        cycle += 1

        # check if interesting cycle
        interesting_cycles = range(20, 220 + 1, 40)
        if cycle in interesting_cycles:
            interesting_cycle.append(cycle * X)

        sprite_position = {X-1, X, X+1}
        if beam_col in sprite_position:
            crt_line += "#"
        else:
            crt_line += " "

        # what happens when cycle completes?
        match instruction:
            case ["noop"]:
                pass
            case ["addx", operand]:
                pipeline.insert(0, f"addx_complete {operand}")
            case ["addx_complete", operand]:
                X += int(operand)
            case _:
                raise Exception("Unknown opcode!")

        # move beam
        beam_col += 1
        if beam_col == 40:
            crt_lines.append(crt_line)
            crt_line = ""
            beam_col = 0
            beam_row += 1

    part1 = sum(interesting_cycle)
    part2 = "\n" + "\n".join(crt_lines)
    return Result(part1, part2)

