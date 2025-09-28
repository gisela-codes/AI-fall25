import argparse
from cs4300_csp_parser import parse_cs4300
from cs4300_csp import solve_backtracking

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run CSP solver")
    parser.add_argument("file", help="Usage: python run_csp.py <problem.csp>")
    parser.add_argument("--mrv", action="store_true")
    args = parser.parse_args()

    csp = parse_cs4300(args.file)

    any_sol = False
    for i, sol in enumerate(solve_backtracking(csp, use_mrv=args.mrv), 1):
        any_sol = True
        print(f"Solution #{i}: {sol}")

    if not any_sol:
        print("No solutions.")