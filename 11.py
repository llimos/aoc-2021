from aocd import lines

# lines = """5483143223
# 2745854711
# 5264556173
# 6141336146
# 6357385478
# 4167524645
# 2176841721
# 6882881134
# 4846848554
# 5283751526""".splitlines()

data = [[int(y) for y in x] for x in lines]

def check_flashes():
    # print('New round')
    # print('\n'.join([''.join([str(y if y < 10 else ('O' if y == 10 else 'X')) for y in x]) for x in data]))
    flashed = 0
    for (x, row) in enumerate(data):
        for (y, octo) in enumerate(row):
            if octo == 10:
                # print((x,y))
                data[x][y] = 11
                flashed += 1
                for dx in range(x-1,x+2):
                    for dy in range(y-1,y+2):
                        if (not (dx == x and dy == y) 
                            and dx >= 0 and dx < len(data)
                            and dy >= 0 and dy < len(data[x])
                            and data[dx][dy] < 10):
                            data[dx][dy] += 1
    return flashed

def do_step():
    # print('New step')
    # Increment everything by 1
    for (x, row) in enumerate(data):
        for (y, octo) in enumerate(row):
            data[x][y] += 1
    # Check for 10's repeatedly until there are no more
    flashed = flashers = check_flashes()
    while flashers > 0:
        flashers = check_flashes()
        flashed += flashers
    # print(already_flashed)
    for (x, row) in enumerate(data):
        for (y, octo) in enumerate(row):
            if octo == 11:
                data[x][y] = 0

    return flashed

total = 0
octopi = len(data) * len(data[0])
i = 0
while (True):
    i += 1
    flashes = do_step()
    total += flashes
    if i == 100:
        print('Part 1', total)
    if flashes == octopi:
        print('Part 2', i)
        break