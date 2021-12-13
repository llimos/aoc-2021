from aocd import data

# data = """6,10
# 0,14
# 9,10
# 0,3
# 10,4
# 4,11
# 6,0
# 6,12
# 4,1
# 0,13
# 10,12
# 3,4
# 3,0
# 8,4
# 1,10
# 2,14
# 8,10
# 9,0

# fold along y=7
# fold along x=5"""

(dots, folding) = [x.splitlines() for x in data.split('\n\n')]
dots = {(int(l.split(',')[0]), int(l.split(',')[1])) for l in dots}
folding = [[x[11],int(x[13:])] for x in folding]

def do_fold(dots, fold):
    (dir, n) = fold
    if dir == 'y':
        # Fold up
        # Anything with y > n, becomes n - (y - n)
        return {(x, y if y < n else n - (y - n)) for (x,y) in dots}
    else:
        # Fold left
        # Anything with x > n, becomes n - (x - n)
        return {(x if x < n else n - (x - n), y) for (x,y) in dots}

print(len(do_fold(dots, folding[0])))

# Part 2
for fold in folding:
    dots = do_fold(dots, fold)

# Print it out
max_x = max([x for (x,y) in dots])
max_y = max([y for (x,y) in dots])

print('\n'.join([''.join(['⬜' if (x,y) in dots else '⬛' for x in range(max_x + 1)]) for y in range(max_y + 1)]))

