from enum import Enum
from typing import Iterator

class OppMove(Enum):
    rock = "A"
    paper = "B"
    scissors = "C"

class MyMove(Enum):
    rock = "X"
    paper = "Y"
    scissors = "Z"

class Outcome(Enum):
    lose = 0
    draw = 3
    win = 6

move_value = {
    MyMove.rock: 1,
    MyMove.paper: 2,
    MyMove.scissors: 3
}

outcome_mapping = {
    OppMove.rock: {
        MyMove.rock: Outcome.draw,
        MyMove.paper: Outcome.win,
        MyMove.scissors: Outcome.lose
    },
    OppMove.paper: {
        MyMove.rock: Outcome.lose,
        MyMove.paper: Outcome.draw,
        MyMove.scissors: Outcome.win
    },
    OppMove.scissors: {
        MyMove.rock: Outcome.win,
        MyMove.paper: Outcome.lose,
        MyMove.scissors: Outcome.draw
    }
}

part2_mapping = {
    MyMove.rock: Outcome.lose,
    MyMove.paper: Outcome.draw,
    MyMove.scissors: Outcome.win
}

def read_file(filename) -> Iterator[str]:
    with open(filename) as input:
        for line in input:
            yield line.strip()

def run() -> None:
    part1_total_score = 0
    part2_total_score = 0
    for line in read_file("input.txt"):
        moves = line.split(" ")
        opp_move = OppMove(moves[0])
        my_move = MyMove(moves[1])

        # part 1
        outcome = outcome_mapping[opp_move][my_move]
        part1_total_score += outcome.value + move_value[my_move]

        # part 2
        outcome_needed = part2_mapping[my_move]
        for move, round_outcome in outcome_mapping[opp_move].items():
            if round_outcome == outcome_needed:
                part2_total_score += outcome_needed.value + move_value[move]
                break

    print(part1_total_score)
    print(part2_total_score)

if __name__ == "__main__":
    run()
