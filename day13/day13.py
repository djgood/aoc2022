from io import TextIOWrapper
from typing import Any, Iterable, Iterator, Optional

from runner import Result
from util import chunked_iterable

from itertools import tee, zip_longest
from functools import cmp_to_key


def parse_packets(input_file: TextIOWrapper) -> Iterator[tuple[Any, Any]]:
    for chunk in chunked_iterable(input_file, 3):
        yield eval(chunk[0].strip()), eval(chunk[1].strip())

def packet_in_order(left_packet: list[Any], right_packet: list[Any]) -> Optional[bool]:
    comparisions = zip_longest(left_packet, right_packet, fillvalue=None)

    for left, right in comparisions:
        if left is None:
            return True

        if right is None:
            return False

        if isinstance(left, int) and isinstance(right, int):
            if left > right:
                return False

            elif left < right:
                return True

        else:
            if isinstance(left, int):
                # print(f"Mixed types; convert {left} to [{left}]")
                left = [left]

            elif isinstance(right, int):
                right = [right]

            subseq_in_order = packet_in_order(left, right)
            if subseq_in_order is not None:
                return subseq_in_order

    return None

def pkt_compare(packet1: list[Any], packet2: list[Any]) -> int:
    cmp = packet_in_order(packet1, packet2)
    if cmp is True:
        return -1
    elif cmp is False:
        return 1
    else:
        return 0

def main(input_file: TextIOWrapper) -> Result:
    indices = []
    sorted_packet_list = []
    for index, packets in enumerate(parse_packets(input_file), start=1):
        in_order_pair = packet_in_order(packets[0], packets[1])
        if in_order_pair is None:
            raise RuntimeError("Did not make decision about packet")
        elif in_order_pair is True:
            indices.append(index)
            sorted_packet_list.append(packets[0])
            sorted_packet_list.append(packets[1])
        else:
            sorted_packet_list.append(packets[1])
            sorted_packet_list.append(packets[0])

    sorted_packet_list += [[[2]], [[6]]]

    sorted_packet_list.sort(key=cmp_to_key(pkt_compare))
    sig1 = sorted_packet_list.index([[2]])
    sig2 = sorted_packet_list.index([[6]])
    decoder_key = (sig1 + 1) * (sig2 + 1)

    return Result(sum(indices), decoder_key)
