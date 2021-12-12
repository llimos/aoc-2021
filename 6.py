from aocd import data

# data = '3,4,3,1,2'

fish = [int(x) for x in data.split(',')]

for i in range(80):
    newfish = []
    for (i,f) in enumerate(fish):
        if f == 0:
            fish[i] = 6
            newfish.append(8)
        else:
            fish[i] -= 1
    fish.extend(newfish)

print(len(fish))

# Part 2

# Keep track of how many of each number there are
fishAges = dict.fromkeys(range(9), 0)
fish = [int(x) for x in data.split(',')]
for f in fish:
    fishAges[f] += 1

for i in range(256):
    newfish = fishAges[0]
    fishAges = {x: fishAges[x + 1] for x in range(8)}
    fishAges[8] = newfish
    fishAges[6] += newfish

print(sum(fishAges.values()))