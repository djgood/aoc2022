from io import TextIOWrapper

from result import Result

def start_packet(line: str) -> int:
    for cursor in range(len(line)):
        if len(set(line[cursor:cursor+4])) == 4:
            return cursor + 4

    return -1

def start_message(line: str) -> int:
    for cursor in range(len(line)):
        if len(set(line[cursor:cursor+14])) == 14:
            return cursor + 14

    return -1

def main(input_file: TextIOWrapper) -> Result:
    line = input_file.readline().strip()
    part1 = start_packet(line)
    part2 = start_message(line)

    return Result(part1, part2)
