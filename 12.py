from aocd import lines

# lines = """dc-end
# HN-start
# start-kj
# dc-start
# dc-HN
# LN-dc
# HN-end
# kj-sa
# kj-HN
# kj-dc""".splitlines()

patharray = [x.split('-') for x in lines]
pathset = [(x,y) for (x,y) in patharray if x != 'end' and y != 'start']
pathset.extend([(y,x) for (x,y) in patharray if x != 'start' and y != 'end'])
print(pathset)
paths: dict[set[str]] = {frm: {y for (x,y) in pathset if x == frm } for (frm,to) in pathset}
print(paths)

def navigate(frm: str = 'start', visited: set = set()):
    if frm[0].islower():
        visited = visited.copy()
        visited.add(frm)
    valid_paths = 0
    for x in paths[frm].difference(visited):
        if x == 'end':
            valid_paths += 1
        else:
            valid_paths += navigate(x, visited)
    return valid_paths


# Start from start and iterate
print(navigate())

# Part 2
def navigate2(frm: str = 'start', visited: set = set(), didTwice = False):
    if frm[0].islower():
        visited = visited.copy()
        visited.add(frm)
    valid_paths = 0
    next = paths[frm].difference(visited) if didTwice else paths[frm]
    for x in next:
        if x == 'end':
            valid_paths += 1
        else:
            valid_paths += navigate2(x, visited, didTwice or x in visited)
    return valid_paths

print(navigate2())