# Advent of Code

These are my solutions for [Advent of Code](https://adventofcode.com/).

## Generating a new solution script

To generate a script for a new problem, run:

```commandline
./gen.py <problem_number> [--year <desired_year>]
```

The `--year` flag is optional; by default the current year will be chosen. The new problem script will be placed in `problems_{desired_year}/{problem_number}.py`.

## Running solution scripts

To run the script for a particular solution part, run:

```commandline
./run.py <problem_number> [-p/--part <part_id>] [-y/--year <desired_year>] [-t/--test OR -r/--real]
```

As before, the `--year` flag is optional and by default the current year will be chosen. The `--part` flag is optional, and by default the script will run all parts.

There's also a shorthand notation so that you can run a part by writing the part after the problem, separated by a period:

```commandline
./run.py <problem_number>.<part_id> [-y/--year <desired_year>]
```

If `-t/--test` is specified, the script will only load test input files, e.g. `./run.py 11 -t` will only load from `11_test.txt` instead of `11.txt`.
