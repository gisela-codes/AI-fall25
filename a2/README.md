# Sliding Tile Puzzle Solver

## Usage
### 1. Solve a single puzzle

Pass the starting state with 9 numbers (0 = blank):

`python3 run.py --heuristic manhattan --start 1 2 3 4 5 6 0 7 8`


Example output:

``` yaml
=== Puzzle: ( 1, 2, 3, 4, 5, 6, 0, 7, 8) ===

--- Manhattan ---
Solution depth: 2
Solution cost: 2
Nodes expanded: 2
Nodes generated: 5
Max frontier size: 3
```
### 2. Run all 30 test puzzles

The file test_puzzle.py defines a list of 30 solvable puzzles. Run them all with:

`python3 run.py --heuristic all --all-tests`


This will evaluate UCS, Misplaced, and Manhattan on each puzzle.

## CLI Options
| Option               | Description                                                 | Example                     | Default             |
| -------------------- | ----------------------------------------------------------- | --------------------------- |---------------------|
| `--start` / `-s`     | Provide 9 integers as the start state                       | `--start 1 2 3 4 5 6 0 7 8` | `0 1 2 3 4 5 6 7 8` |
| `--heuristic`        | Choose heuristic: `ucs`, `misplaced`, `manhattan`, or `all` | `--heuristic manhattan`     | `all`               |
| `--all-tests`        | Run all 30 test puzzles from                                | `--all-tests`               |                     |