
# RULES
# farmer CAN go alone 
# NOT (0,X,1,1) - goat & cabbage can't be together
# NOT (0,1,1,X) - wolf & goat can't be together 

# what this should do 
# (0,0,0,0), (1,0,1,0), (0,0,1,0), (1,1,1,0), (0,1,0,0), (1,1,0,1), (0,1,0,1), (1,1,1,1)
def wgc_actions(state):
    neighbors = []
    f,w,g,c = state

    neighbors.append((1-f,w,g,c))

    if f == w:
        neighbors.append((1-f,1-w,g,c))
    if f == g:
        neighbors.append((1-f,w,1-g,c))
    if f == c:
        neighbors.append((1-f, w,g,1-c))

    actions = []

    for n in neighbors:
        f,w,g,c = n
        if f != w == g:
            continue
        if f != g == c:
            continue
        actions.append(n)
        
    return actions