from aocd import lines

# lines = """0,9 -> 5,9
# 8,0 -> 0,8
# 9,4 -> 3,4
# 2,2 -> 2,1
# 7,0 -> 7,4
# 6,4 -> 2,0
# 0,9 -> 2,9
# 3,4 -> 1,4
# 0,0 -> 8,8
# 5,5 -> 8,2""".splitlines()

points = [[0] * 1000 for i in range(1001)]

for line in lines:
    # Find the points
    (start, end) = line.split(' -> ')
    (x1,y1) = [int(x) for x in start.split(',')]
    (x2,y2) = [int(x) for x in end.split(',')]

    # Part 1: Horizontal or vertical only
    # if x1 != x2 and y1 != y2:
    #     continue

    # Special case: vertical line
    if x2 == x1:
        for curY in range(y1, y2 + 1 if y2 > y1 else y2 - 1, 1 if y2 > y1 else -1):
            points[x1][curY] += 1
    else:
        # Find the gradient
        gradient = (y2 - y1) / (x2 - x1)

        # Iterate x to get all the points
        curX = x1
        for curX in range(x1, x2 + 1 if x2 > x1 else x2 - 1, 1 if x2 > x1 else -1):
            points[curX][y1 + int((curX - x1) * gradient)] += 1

# See how many points have more than 2
print( sum( 
    [ len([x for x in row if x > 1]) for row in points ] 
) )
