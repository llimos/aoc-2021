from functools import reduce
from typing import Set
from aocd import lines

# lines = """2199943210
# 3987894921
# 9856789892
# 8767896789
# 9899965678""".splitlines()

cells = [[int(y) for y in x] for x in lines]

def islowest(x,y):
    n = cells[x][y]
    if x > 0 and cells[x-1][y] <= n: return False
    if y > 0 and cells[x][y-1] <= n: return False
    if x < len(cells) - 1 and cells[x+1][y] <= n: return False
    if y < len(cells[x]) - 1 and cells[x][y+1] <= n: return False
    return True

score = 0
for (xi,x) in enumerate(cells):
    for (yi,y) in enumerate(x):
        if islowest(xi,yi): score += (y + 1)

print(score)

# Part 2

seen = set()

def followbasin(x, y):
    n = 0
    # DFS - go all the way left, then iterate right, for each one go down and repeat
    # Attempt to go left
    if y > 0 and cells[x][y - 1] != 9 and (x, y - 1) not in seen: 
        return followbasin(x, y - 1)
    # If not, mark this cell
    n += 1
    seen.add((x, y))
    # Attempt to go up
    if x > 0 and cells[x - 1][y] != 9 and (x - 1, y) not in seen:
        n += followbasin(x - 1, y)
    # Attempt to go down
    if x < len(cells) - 1 and cells[x + 1][y] != 9 and (x + 1, y) not in seen:
        n += followbasin(x + 1, y)
    # If not, go right
    if y < len(cells[x]) - 1 and cells[x][y + 1] != 9 and (x, y + 1) not in seen:
        n += followbasin(x, y + 1)
    
    # If no more right, return
    return n

# Start at top-left
# Find the first cell that is part of a basin
basins = []
for (x,row) in enumerate(cells):
    for (y,v) in enumerate(row):
        if v == 9: continue
        if (x,y) in seen: continue
        # If we're here, this is the start of a new basin
        basins.append(followbasin(x, y))

basins.sort()
basins.reverse()
print(basins[0:3], reduce(lambda x, y: x * y, basins[0:3], 1))