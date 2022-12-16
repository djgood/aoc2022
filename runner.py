#!python3

import click
from pathlib import Path
import importlib
import os
from typing import List, Optional

from result import Result

DAY_DIR_PATH = "./day{n}/"
SAMPLE_INPUT_PATH = DAY_DIR_PATH + "sample_input.txt"
INPUT_PATH = DAY_DIR_PATH + "input.txt"
PROGRAM_MODULE = "day{n}.day{n}"

def collect_input(input_name: str, input_path: Path, input_page: Optional[str] = None)-> bool:
    if input_path.exists():
        if not click.confirm(f"Overwrite the existing path ({input_path})?"):
            return False

    if input_page:
        os.system(f"open '{input_page}'")
    sample = click.edit(input_name)
    with open(input_path, "w") as file_handle:
        file_handle.write(sample)

    return True

def stub_main() -> Result:
    return Result(None, None)

def run_main(day: int, input_path: Path) -> Result:
    day_module = importlib.import_module(PROGRAM_MODULE.format(n=day))
    main = getattr(day_module, "main")
    with open(input_path) as puzzle_input:
        return main(puzzle_input)

@click.group()
def cli():
    pass

@cli.command(help="Initialize day N")
@click.argument(
    "n",
    type=int
)
def init(n: int):
    if n < 1 or n > 25:
        click.echo("Invalid day specified. Puzzle series ends on 25")
        return

    day_path = Path(DAY_DIR_PATH.format(n=n))
    if not day_path.exists():
        day_path.mkdir()

    if collect_input(
        "Sample puzzle input",
        Path(SAMPLE_INPUT_PATH.format(n=n)),
        f"https://adventofcode.com/2022/day/{n}"
    ) is False:
        click.echo(f"Skipped sample input for day {n}")

    if collect_input(
        "Input",
        Path(INPUT_PATH.format(n=n)),
        f"https://adventofcode.com/2022/day/{n}/input"
    ) is False:
        click.echo(f"Skipped input for day {n}")

    os.system(f"cp dayN.py.template {day_path}/day{n}.py")
    print(f"Day {n} initialized.")

@cli.command(help="Run ./day[N]/day[N].py against the sample puzzle input. Defaults to ./day[N]/sample_input.txt")
@click.argument(
    "n",
    type=int
)
@click.option(
    "--test-file", "-f",
    type=click.Path(exists=False),
    help="Test against a specific file. Will ask for input if the file doesn't exist."
)
def test(n: int, test_file: Optional[str]):
    if test_file:
        test_file_path = Path(test_file)
        collect_input(
            "Test file",
            test_file_path
        )
    else:
        test_file_path = Path(SAMPLE_INPUT_PATH.format(n=n))

    if not test_file_path.exists():
        click.echo(f"Error: Day {n} not initialized.")
        return

    result = run_main(day=n, input_path=test_file_path)
    click.echo(result)

@cli.command(help="Run ./day[N]/day[N].py against the real puzzle input.")
@click.argument("n", nargs=-1, type=str)
def run(n: List[int]):
    n = [int(day) for day in n]
    for day in n:
        if len(n) > 1:
            click.echo(f"=== Day {day} ===")

        puzzle_input = Path(INPUT_PATH.format(n=day))
        if not puzzle_input.exists():
            click.echo(f"Error: Day {day} not initialized.")
            return

        result = run_main(day=day, input_path=puzzle_input)
        click.echo(str(result))

if __name__ == "__main__":
    cli()
