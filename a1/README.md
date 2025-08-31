# AI-fall25
## Assignment 1 - Using BFS and IDS for the Wolf Goat Cabbage problem
### State Representation

Each state is represented as a list of four binary values:

```
[f, w, g, c]
```

* `f` = Farmer
* `w` = Wolf
* `g` = Goat
* `c` = Cabbage
* `0 = left bank`, `1 = right bank`

Example:

* `[0,0,0,0]` → all are on the left bank
* `[1,1,1,1]` → all are on the right bank

---

### How to Run

```bash
python3 run.py -a <algorithm> -s <start_state> -g <goal_state>
```

#### Arguments

| Option    | Shorthand | Choices             | Description             |
| --------- | --------- | ------------------- | ----------------------- |
| `--algo`  | `-a`      | `bfs`, `ids`, `all` | Choose search algorithm |
| `--start` | `-s`      | 4 integers (0/1)    | Start state             |
| `--goal`  | `-g`      | 4 integers (0/1)    | Goal state              |

### Example

Run BFS from `[0,0,0,0]` to `[1,1,1,1]`:

```bash
python3 run.py -a bfs -s 0 0 0 0 -g 1 1 1 1
```

Run IDS:

```bash
python3 run.py -a ids -s 0 0 0 0 -g 1 1 1 1
```

Run both BFS and IDS:

```bash
python3 run.py -a all -s 0 0 0 0 -g 1 1 1 1
```

---

### Output

The output is the path of `(state, action)` steps to goal:

```
Domain: WGC | Algorithm: BFS
Solution cost: 6 | Depth: 6
Nodes generated: 19 | Nodes expanded: 10 | Max frontier: 2
Path:
    Step 1) (0, 0, 0, 0) --> (1, 0, 1, 0)

    Step 2) (1, 0, 1, 0) --> (0, 0, 1, 0)

    Step 3) (0, 0, 1, 0) --> (1, 1, 1, 0)

    Step 4) (1, 1, 1, 0) --> (0, 1, 0, 0)

    Step 5) (0, 1, 0, 0) --> (1, 1, 0, 1)

    Step 6) (1, 1, 0, 1) --> (0, 1, 0, 1)

    Step 7) (0, 1, 0, 1) --> (1, 1, 1, 1)


Domain: WGC | Algorithm: IDS
Solution cost: 6 | Depth: 6
Nodes generated: 61 | Nodes expanded: 42 | Max frontier: 9
Path:
    Step 1) (0, 0, 0, 0) --> (1, 0, 1, 0)

    Step 2) (1, 0, 1, 0) --> (0, 0, 1, 0)

    Step 3) (0, 0, 1, 0) --> (1, 1, 1, 0)

    Step 4) (1, 1, 1, 0) --> (0, 1, 0, 0)

    Step 5) (0, 1, 0, 0) --> (1, 1, 0, 1)

    Step 6) (1, 1, 0, 1) --> (0, 1, 0, 1)

    Step 7) (0, 1, 0, 1) --> (1, 1, 1, 1)
```


