# Advent of Code 2022 Solutions

Janky solutions to the [Advent of Code](https://adventofcode.com/2022)

## Overview

```
./runner.py --help
```

## Initialize a day

Initialized all required files for a day. Automatically opens to the Advent of
Code web page. Prompts for the sample input and puzzle input and writes to
disk.

```
`./runner.py init <day>`
```

## Test

Run the puzzle solution for the day against the sample input. Uses
`sample_input.txt` for the day by default. Possible to test against a custom
file with `--test-file <file_name>`.

```
`./runner.py test <day>`
```

## Run

Run the puzzle solution against the input.

```
./runner run <day>
```
