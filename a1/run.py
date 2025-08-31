import argparse
from search_core import *
from domains.wgc import *


def main():
    parser = argparse.ArgumentParser(
        description="Run search algorithms using the WGC domain"
    )
    parser.add_argument(
        "--domain", "-d",
        choices=["wgc, jugs"],
        default="wgc",
    )
    parser.add_argument(
        "--algo", "-a",
        choices=["bfs", "ids", "all"],
        default="all",
        help="Algorithm to run (bfs or ids)"
    )
    parser.add_argument(
        "--start", "-s",
        type=int,
        nargs=4,
        default=[0, 0, 0, 0],
        help="Choose Start State"
    )
    parser.add_argument(
        "--goal", "-g",
        type=int,
        nargs=4,
        default=[1, 1, 1, 1],
        help="Choose Goal Test"

    )
    args = parser.parse_args()
    start = tuple(args.start)
    goal = tuple(args.goal)

    if args.domain == "wgc":
        domain = wgc_actions

    if args.domain == "jugs":
        print("That hasn't been implemented (yet)")
    if args.algo == "bfs" or args.algo == "all":
        path, g, e, f = bfs(start, goal, domain)
        print(f'''
            Domain: WGC | Algorithm: BFS
            Solution cost: {len(path) - 1} | Depth: {len(path) - 1}
            Nodes generated: {g} | Nodes expanded: {e} | Max frontier: {f}
            Path:''')
        for p in range(len(path)): 
            state, action = path[p]
            print(f'\t\tStep {p+1})\t{state} --> {action}\n')

        print(f'''
            Domain: WGC | Algorithm: IDS
            Solution cost: {len(path) - 1} | Depth: {len(path) - 1}
            Nodes generated: {g} | Nodes expanded: {e} | Max frontier: {f}
            Path:''')
        for p in range(len(path)): 
            state, action = path[p]
            print(f'\t\tStep {p+1})\t{state} --> {action}\n')
                

#python3 run.py -a ids    
if __name__ == "__main__":
    main()
