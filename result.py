from dataclasses import dataclass
from typing import Any

@dataclass()
class Result:
    part1: Any
    part2: Any

    def __str__(self) -> str:
        return f"Part 1: {self.part1}\nPart 2: {self.part2}"
