from dataclasses import dataclass
from functools import reduce
import itertools
import operator
from typing import Iterator, List

def read_input(filename):
    with open(filename) as file:
        for line in file:
            yield line.strip()

def grouper(n, iterable):
    it = iter(iterable)
    while True:
        chunk = tuple(itertools.islice(it, n))
        if not chunk:
            return
        yield chunk

@dataclass
class Test:
    divisible: int
    true: int
    false: int

class Monkey:
    def __init__(self, starting_items: List[int], op: str, test: Test) -> None:
        self.items = starting_items
        self.op = op
        self.test = test
        self.items_inspected = 0

def read_monkeys(input: Iterator[str]) -> Iterator[Monkey]:
    for text in grouper(7, input):
        items = [int(item) for item in text[1].strip("Starting items: ").split(", ")]
        operation = text[2][len("Operation: new = old "):]
        divisible = int(text[3][len("Test: divisible by "):])
        if_true = int(text[4][len("If true: throw to monkey "):])
        if_false = int(text[5][len("If false: throw to monkey "):])
        test = Test(divisible, if_true, if_false)
        yield Monkey(items, operation, test)

def monkey_sim(rounds: int, alternate_worry: bool = False):
    monkeys = list(read_monkeys(read_input(("sample_input.txt"))))

    mcd = reduce(operator.mul, [monkey.test.divisible for monkey in monkeys], 1)
    for _ in range(rounds):
        for monkey in monkeys:
            while monkey.items:
                new = None
                old = monkey.items.pop(0)
                operation = monkey.op.split(" ")
                match operation:
                    case ["*", "old"]:
                        new = old * old
                    case ["*", operand]:
                        new = old * int(operand)
                    case ["+", operand]:
                        new = old + int(operand)
                    case _:
                        raise Exception(f"Woah! {monkey.op}")

                monkey.items_inspected += 1
                if not alternate_worry:
                    new = int(new/3)
                else:
                    new = new % mcd

                if new % monkey.test.divisible == 0:
                    new_i = monkey.test.true
                else:
                    new_i = monkey.test.false

                monkeys[new_i].items.append(new)

    most_inspected = sorted([monkey.items_inspected for monkey in monkeys])[-2:]
    return most_inspected[0] * most_inspected[1]

def main():
    print("part1:", monkey_sim(rounds=20))
    print("part2:", monkey_sim(rounds=10000, alternate_worry=True))

if __name__ == "__main__":
    main()
