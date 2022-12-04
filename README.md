# Advent of Code

These are my solutions for [Advent of Code](https://adventofcode.com/).

## Generating a new solution script

To generate a script for a new day, run:

```commandline
./gen.py <day> [--year <desired_year>]
```

The `--year` flag is optional; by default the current year will be chosen. The new script will be placed in `problems_{desired_year}/{day}.py`.

## Running solution scripts

To run the script for a particular problem, run:

```commandline
./run.py <day>[.<part_id>] [-y/--year <desired_year>] [-t/--test]
```

As before, the `--year` flag is optional and by default the current year will be chosen. The `part_id` is optional, and by default the script will run all parts. You can run multiple days/parts:

```commandline
./run.py 1 2.1 3 4.1 4.1_alternative
```

If `-t/--test` is specified, the script will only load test input files, e.g. `./run.py 11 -t` will only load from `11_test.txt` instead of `11.txt`.

You can also run all problems for a given year:

```commandline
./run.py [-a/-all] [-y/--year <desired_year>]
```
