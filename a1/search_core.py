from queue import Queue

def bfs(start, goal, gen_actions):
    q = Queue()
    q.put([(start), [start]])
    visited = set([start])

    generated = 0
    expanded = 0
    max_frontier = 0

    while not q.empty():
        max_frontier = max(max_frontier, q.qsize())

        state, path = q.get()
        expanded += 1   # expanded a node

        if state == goal:
            return path, generated, expanded, max_frontier

        actions = gen_actions(state)

        for a in actions:
            generated += 1 
            if a not in visited:
                # print('add to queue:', a, path + [a])
                visited.add(a)
                q.put((a, path + [a]))

def depth_limited_dfs(state, goal, limit, path, visited, gen_actions):
    expanded = 1   # visiting this node
    generated = 0
    max_frontier = len(visited)
    if state == goal:
            return path, expanded, generated, max_frontier
    if limit == 0:
        return None, generated, expanded, max_frontier
    actions = gen_actions(state)

    for a in actions:
        generated += 1
        if a not in visited:
            visited.add(a)
            found_path, g, e, m = depth_limited_dfs(a, goal, limit - 1, path + [a], visited, gen_actions)
            generated += g
            expanded += e
            max_frontier = max(max_frontier, m)
            if found_path:
                return found_path, generated, expanded, max_frontier

    return None, generated, expanded, max_frontier

def ids(start, goal, gen_actions):
    depth_limit = 0
    generated = 0
    expanded = 0
    max_frontier = 0
    while True:
        found_path, g, e, m = depth_limited_dfs(start, goal, depth_limit, [start], set([start]), gen_actions)

        generated += g
        expanded += e
        max_frontier = max(max_frontier, m)

        if found_path:
            return found_path, generated, expanded, max_frontier
        depth_limit += 1