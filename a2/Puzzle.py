import heapq

def InitialState(state):
    return state

def Actions(state):
    pos = state.index(0)
    adj = {0:[1,3], 1:[0,2,4], 2:[1,5], 3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8], 6:[3,7], 7:[4,6,8], 8:[5,7]}
    return adj[pos]

def Transition(state, action):
    pos = state.index(0)
    new_state = list(state)
    new_state[pos] = state[action]
    new_state[action] = 0
    return tuple(new_state)

def GoalTest(state):
    # check if the current state is the goal
    if state == (1,2,3,4,5,6,7,8,0):
        return True
    return False

def StepCost(state, action, next_state):
    return 1

def Manhattan(state):
    manhattan = 0
    for i in range(9): 
        t = state[i]
        if t == 0:  
            continue
        row, col = divmod(i, 3)
        goal_row, goal_col = divmod(t-1, 3) #t -1 is the index of where the tile goes
        manhattan += abs(row - goal_row) + abs(col - goal_col)
    return manhattan

def Misplaced(state):
    misplaced = 0
    for i in range(9): 
        tile = state[i]
        if tile != 0 and tile != i + 1:  
            misplaced += 1
    return misplaced

def UCS(state):
    return 0

def astar(start, heuristic):
    frontier = [(heuristic(start), 0, start)]
    came_from = {} 
    best_g = {start: 0}
    nodes_expanded = 0          
    nodes_generated = 0         
    max_frontier_size = 1

    while frontier:
        f, g, s = heapq.heappop(frontier)
        if g != best_g.get(s, float('inf')):
            continue
        if GoalTest(s):
            # reconstruct path from start to s
            path = [s]
            while path[-1] in came_from:
                path.append(came_from[path[-1]])
            stats = {
                "nodes_expanded": nodes_expanded,
                "nodes_generated": nodes_generated,
                "max_frontier_size": max_frontier_size,
                "solution_depth": len(path) - 1,
                "solution_cost": best_g[s]
            }
            return list(reversed(path)), stats
        nodes_expanded +=1
        for a in Actions(s):
            ns = Transition(s, a)
            ng = g + StepCost(s, a, ns)
            nodes_generated +=1

            if ng < best_g.get(ns, float('inf')):
                best_g[ns] = ng
                came_from[ns] = s
                heapq.heappush(frontier, (ng + heuristic(ns), ng, ns))

        if len(frontier) > max_frontier_size:
            max_frontier_size = len(frontier)
    return None, {
        "nodes_expanded": nodes_expanded,
        "nodes_generated": nodes_generated,
        "max_frontier_size": max_frontier_size,
        "solution_depth": None,
        "solution_cost": None
    }

