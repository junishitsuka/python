# coding: UTF-8
# pythonのversion対応
try:
    from Queue import Queue
except ImportError:
    from queue import Queue

def checkio(maze_map):
    start = [1, 1]
    end = [10, 10]
    q = Queue()
    visited = {}
    parent = {}
    str = ''
    visited["%d,%d" % (start[0],start[1])] = True
    parent["%d,%d" % (start[0],start[1])] = None
    q.put(start)
    while (not(q.empty())):
        tmp = q.get()
        if (tmp == end): break
        up = [(tmp[0] - 1), tmp[1]]
        down = [(tmp[0] + 1), tmp[1]]
        right = [tmp[0], (tmp[1] + 1)]
        left = [tmp[0], (tmp[1] -1)]
        if (maze_map[up[0]][up[1]] == 0 and visited.get("%d,%d" % (up[0],up[1])) != True):
            visited["%d,%d" % (up[0],up[1])] = True
            q.put(up)
            parent["%d,%d" % (up[0],up[1])] = tmp
        if (maze_map[down[0]][down[1]] == 0 and visited.get("%d,%d" % (down[0],down[1])) != True):
            visited["%d,%d" % (down[0],down[1])] = True
            q.put(down)
            parent["%d,%d" % (down[0],down[1])] = tmp
        if (maze_map[right[0]][right[1]] == 0 and visited.get("%d,%d" % (right[0],right[1])) != True):
            visited["%d,%d" % (right[0],right[1])] = True
            q.put(right)
            parent["%d,%d" % (right[0],right[1])] = tmp
        if (maze_map[left[0]][left[1]] == 0 and visited.get("%d,%d" % (left[0],left[1])) != True):
            visited["%d,%d" % (left[0],left[1])] = True
            q.put(left)
            parent["%d,%d" % (left[0],left[1])] = tmp

    target = [end[0], end[1]]
    while (not(parent.get("%d,%d" % (target[0],target[1])) == None)):
        par = parent["%d,%d" % (target[0],target[1])]
        if (target[0] == par[0] + 1): str = 'S' + str 
        if (target[0] == par[0] - 1): str = 'N' + str
        if (target[1] == par[1] + 1): str = 'E' + str
        if (target[1] == par[1] - 1): str = 'W' + str
        target = par
	
    print str
	
    return str

# test
checkio([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 1],
        [1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1],
        [1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])
