from io import TextIOWrapper
from typing import Any, Iterable, Iterator, Optional

from runner import Result
from util import chunked_iterable

from itertools import tee, zip_longest


def parse_packets(input_file: TextIOWrapper) -> Iterator[Iterator[tuple[Any,Any]]]:
    for chunk in chunked_iterable(input_file, 3):
        print(chunk[0].strip())
        print(chunk[1].strip())
        yield zip_longest(eval(chunk[0].strip()), eval(chunk[1].strip()), fillvalue=None)

def packet_in_order(packets: Iterable[tuple[Any, Any]]) -> Optional[bool]:
    for left, right in packets:
        print(f"Compare {left} vs {right}")
        if left is None:
            print("Left side ran out of items")
            return True

        if right is None:
            print("Right side ran out of items")
            return False

        if isinstance(left, int) and isinstance(right, int):
            if left > right:
                print("Left side is bigger, so inputs are NOT in the right order")
                return False

            elif left < right:
                print("Left side is smaller, so inputs are in the right order")
                return True

        else:
            if isinstance(left, int):
                # print(f"Mixed types; convert {left} to [{left}]")
                left = [left]

            elif isinstance(right, int):
                right = [right]

            subseq_in_order = packet_in_order(zip_longest(left, right, fillvalue=None))
            if subseq_in_order is not None:
                return subseq_in_order
            else:
                print("Did not make a decision")

    return None

def main(input_file: TextIOWrapper) -> Result:
    indices = []
    for index, packets in enumerate(parse_packets(input_file), start=1):
        in_order = packet_in_order(packets)
        if in_order is None:
            raise RuntimeError("Did not make decision about packet")
        elif in_order is True:
            indices.append(index)

    print(indices)
    return Result(sum(indices), None)
