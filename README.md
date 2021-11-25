# Advent of Code

These are my solutions for [Advent of Code](https://adventofcode.com/).

## Generating a new solution script

To generate a script for a new problem, run:

```commandline
python gen.py <problem_number> [--year <desired_year>]
```

The `--year` flag is optional; by default the current year will be chosen. The new problem script will be placed in `problems_{desired_year}/{problem_number}.py`.

## Running solution scripts

To run the script for a particular solution part, run:

```commandline
python run.py <problem_number> <part_number> [--year <desired_year>]
```

As before, the `--year` flag is optional and by default the current year will be chosen.
