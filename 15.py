from aocd import lines
from sys import _current_frames, maxsize, setrecursionlimit
from heapq import heappush, heappop

setrecursionlimit(1500)

# lines = """1163751742
# 1381373672
# 2136511328
# 3694931569
# 7463417111
# 1319128137
# 1359912421
# 3125421639
# 1293138521
# 2311944581""".splitlines()

data = [[int(y) for y in x] for x in lines]


# Dijkstra

visited: set[tuple[int, int]] = set()
distances: dict[tuple[int, int], int] = {(0,0): 0}
to_visit: list[int, int, int] = [(0, 0, 0)]

while len(to_visit):
    (d, y, x) = heappop(to_visit)
    visited.add((y,x))
    to_try = ([y+1, x], [y, x+1], [y-1, x], [y, x-1])
    for (ty, tx) in to_try:
        if (ty,tx) in visited or ty < 0 or ty >= len(data) or tx < 0 or tx >= len(data[y]):
            continue
        # Update the cost
        # Find existing
        existing = distances.get((ty, tx))
        # Find new
        newdist = distances[(y, x)] + data[ty][tx]
        
        if existing == None or newdist < existing:
            distances[ty, tx] = newdist
            heappush(to_visit, (newdist, ty, tx))
print(distances[(len(data) - 1, len(data[len(data)-1])-1)])

# PART 2
visited: set[tuple[int, int]] = set()
distances: dict[tuple[int, int], int] = {(0,0): 0}
to_visit: list[int, int, int] = [(0, 0, 0)]

while len(to_visit):
    (d, y, x) = heappop(to_visit)
    visited.add((y,x))
    to_try = ([y+1, x], [y, x+1], [y-1, x], [y, x-1])
    for (ty, tx) in to_try:
        if (ty,tx) in visited or ty < 0 or ty >= len(data) * 5 or tx < 0 or tx >= len(data[0]) * 5:
            continue
        # Update the cost
        # Find existing
        existing = distances.get((ty, tx))
        # Find new
        basescore = data[ty % len(data)][tx % len(data[0])]
        multiplier = int((ty)/len(data)) + int((tx)/len(data[0]))
        cellvalue = ((basescore - 1 + multiplier) % 9) + 1
        newdist = distances[(y, x)] + cellvalue
        
        if existing == None or newdist < existing:
            distances[ty, tx] = newdist
            heappush(to_visit, (newdist, ty, tx))
print(distances[((len(data)*5) - 1, (len(data[0])*5)-1)])


exit()

# Previous attempts:

# Memoization
best_from: dict[int, dict[int, int]] = {len(data)-1: {len(data[0])-1: 0}}

recursion = 0

def nav(y: int, x: int, visited: set[tuple[int, int]] = set(), bail_at: int = maxsize):
    global best_from, recursion
    recursion += 1
    # print(recursion, y, x, bail_at, visited)
    # Check if reached destination
    if y == len(data) - 1 and x == len(data[y]) - 1:
        # print('Found')
        recursion -= 1
        return 0
    # Check if we have cached result
    if y in best_from and x in best_from[y]:
        recursion -= 1
        return best_from[y][x]
    # Check if busted or been here before - this is clearly not the fastest route
    if data[y][x] > bail_at or (y,x) in visited:
        # print('Bailing -', data[y][x], 'is more than', bail_at)
        recursion -= 1
        return None
    else:
        bail_at -= data[y][x]
    
    # Otherwise, start trying
    new_visited = visited.union([(y,x)])

    best = None
    to_try = ([y+1, x], [y, x+1], [y-1, x], [y, x-1])
    for (ty, tx) in to_try:
        if ty >= 0 and ty < len(data) and tx >= 0 and tx < len(data[ty]):
            new_bail_at = min(bail_at, best) if best else bail_at
            res = nav(ty, tx, new_visited, new_bail_at)
            if res != None:
                res += data[ty][tx]
                if best == None or res < best:
                    best = res
    
    # Return min
    # if best:
    #     best_from.setdefault(y, dict())[x] = best
    # else:
    #     print('Giving up')
    recursion -= 1
    return best

# Since we're hitting recursion limits, let's populate the table first, starting from the bottom right
# We want to fan out from the corner
n = len(data)
while n > 0:
    n -= 1
    # We want to do (99,99) (99,98) (98,99) (99,97) (97,99) (98,97) (97,98) (97,97)
    for counterpart in range(len(data)-1, n-1, -1):
        if n < len(data) and counterpart < len(data[n]):
            res = nav(n, counterpart)
            best_from.setdefault(n, dict())[counterpart] = res
            print(n,counterpart,res)
        if n != counterpart and counterpart < len(data) and n < len(data[counterpart]):
            res = nav(counterpart, n)
            best_from.setdefault(counterpart, dict())[n] = res
            print(counterpart,n,res)


# y = len(data)
# while y > 0:
#     y -= 1
#     x = len(data[y])
#     while x > 0:
#         x -= 1
#         res = nav(y,x)
#         best_from.setdefault(y, dict())[x] = res
#         print(y, x, res)

# Now do it again, and see if you can beat the old one by going up and down too. If you can't, bail

# def nav2(y: int, x: int, visited: set[tuple[int, int]] = set(), bail_at: int = maxsize):
#     global lowest, best_from, recursion
#     recursion += 1
#     print(recursion, y, x, len(visited))
#     # Check if reached destination
#     if y == len(data) - 1 and x == len(data[y]) - 1:
#         recursion -= 1
#         return 0
#     # Check if busted
#     if bail_at < 0:
#         print('Bailing -', data[y][x], 'is more than', bail_at)
#         recursion -= 1
#         return None
#     else:
#         bail_at -= data[y][x]
    
#     # Otherwise, start trying
#     new_visited = visited.union([(y,x)])

#     best = None
#     to_try = ([y+1, x], [y, x+1], [y-1, x], [y, x-1])
#     for (ty, tx) in to_try:
#         if ty >= 0 and ty < len(data) and tx >= 0 and tx < len(data) and (ty, tx) not in visited:
#             new_bail_at = min(bail_at, best) if best else bail_at
#             res = data[ty+1][tx] + nav(ty, tx, new_visited, new_bail_at)
#             if res and (not best or res < best):
#                 best = res
#     # best = min(best, data[y+1][x] + nav(y + 1, x, new_visited, min(bail_at, best)) if y < len(data) - 1 and (y+1,x) not in visited else maxsize)
#     # best = min(best, data[y][x+1] + nav(y, x + 1, new_visited, min(bail_at, best)) if x < len(data[y]) - 1 and (y,x+1) not in visited else maxsize)
#     # best = min(best, data[y-1][x] + nav(y - 1, x, new_visited, min(bail_at, best)) if y > 0 and (y-1,x) not in visited else maxsize)
#     # best = min(best, data[y][x-1] + nav(y, x - 1, new_visited, min(bail_at, best)) if x > 0 and (y,x-1) not in visited else maxsize)
    
#     # Return min
#     if best:
#         best_from.setdefault(y, dict())[x] = best
#     recursion -= 1
#     return best

# y = len(data)
# while y > 0:
#     y -= 1
#     x = len(data[y])
#     while x > 0:
#         x -= 1
#         nav2(y, x, set(), best_from[y][x])

print(nav(0,0))