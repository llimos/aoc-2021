from aocd import data

# data = '16,1,2,0,4,2,7,1,2,14'

positions = [int(x) for x in data.split(',')]

def total(steps):
    return (steps + 1) * (steps / 2)

print(min([
    sum( [total(abs(p - x)) for x in positions] )
    for p in range(min(positions), max(positions)+1)
]))


