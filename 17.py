from aocd import data
import re

r = re.compile('target area: x=(?P<x1>-?\d+)..(?P<x2>-?\d+), y=(?P<y1>-?\d+)..(?P<y2>-?\d+)')
m = r.match(data)
x1 = int(m.group('x1'))
x2 = int(m.group('x2'))
y1 = int(m.group('y1'))
y2 = int(m.group('y2'))

# Part 1 - only interested in y (x and y do not affect each other)
# Each step, y increases by dy and dy decreases by 1
# y = y + dy, dy -= 1
# y + dy + dy-1 + dy-2 + dy-3
# after n steps: n.dy - n-1

# Goal is to get to (presumably) the higher of y1, y2
goal = max(y1, y2)
print(goal)

# Goal is -58 
# Once it hits the top of the parabola (dy = 0), it comes down in 1 + 2 + 3 + 4 etc. steps
# To find how many steps that is, reverse max+min * steps/2 = 58
# max+min * steps = 116
# steps = 116 / max+min
# max = 