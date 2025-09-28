import argparse
from puzzle import *
from test_puzzle import solvable_30
def main():
    parser = argparse.ArgumentParser(
        description="8 Puzzle Solver"
    )
    parser.add_argument(
        "--start", "-s",
        type=int,
        nargs=9,
        default=[0,1,2,3,4,5,6,7,8],
        help="Single start state, 9 numbers separated by space"
    )
    parser.add_argument("--all-tests", action="store_true",help="Run all 30 test puzzles")
    parser.add_argument(
        "--heuristic", 
        choices=["ucs", "misplaced", "manhattan", "all"],
        default="all"
    )
    args = parser.parse_args()

    if args.all_tests:
        puzzles = solvable_30
    else:
        puzzles = [tuple(args.start)]

    heuristics = {}
    if args.heuristic in ("ucs", "all"):
        heuristics["UCS"] = UCS
    if args.heuristic in ("misplaced", "all"):
        heuristics["Misplaced"] = Misplaced
    if args.heuristic in ("manhattan", "all"):
        heuristics["Manhattan"] = Manhattan

    for puzzle in puzzles:
        print(f"\n=== Puzzle: {puzzle} ===")
        for name, heuristic in heuristics.items():
            path, stats = astar(puzzle, heuristic)
            print(f"\n--- {name} ---")
            print(f"Solution depth: {stats['solution_depth']}")
            print(f"Solution cost: {stats['solution_cost']}")
            print(f"Nodes expanded: {stats['nodes_expanded']}")
            print(f"Nodes generated: {stats['nodes_generated']}")
            print(f"Max frontier size: {stats['max_frontier_size']}")

if __name__ == "__main__":
    main()