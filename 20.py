from aocd import data

# data ="""..#.#..#####.#.#.#.###.##.....###.##.#..###.####..#####..#....#..#..##..###..######.###...####..#..#####..##..#.#####...##.#.#..#.##..#.#......#.###.######.###.####...#.##.##..#..#..#####.....#.#....###..#.##......#.....#..#..#..##..#...##.######.####.####.#.#...#.......#..#.#.#...####.##.#......#..#...##.#.##..#...##.#.##..###.#......#.#.......#.#.#.####.###.##...#.....####.#..#..#.##.#....##..#.####....##...##..#...#......#.#.......#.......##..####..#...#.#.#...##..#.#..###..#####........#..####......#..#

# #..#.
# #....
# ##..#
# ..#..
# ..###"""

algo, image = data.split('\n\n')

image = [list(x) for x in image.splitlines()]

def process(image: list[list[str]], extrafill: str = '.') -> list[list[str]]:
    # Need to expand image by 1 extra rows and columns (of blanks) on each side
    # and there will be 1 more extra row and col of zeroes
    
    # First rows
    rowlength = len(image[0])
    image.insert(0, [extrafill for x in range(rowlength)])
    image.append([extrafill for x in range(rowlength)])

    # Now columns
    for y,row in enumerate(image):
        row.insert(0, extrafill)
        row.append(extrafill)
        image[y] = row
    
    # Now we can process
    newimage = []
    for y,row in enumerate(image):
        newimage.append([])
        for x,cell in enumerate(row):
            binary = ''
            for dy in range(y-1, y+2):
                for dx in range(x-1, x+2):
                    # Since 0 = # and 2^9 = ., we need to realise that all the infinite ones will be flipped every turn
                    if dy >= 0 and dy < len(image) and dx >= 0 and dx < len(image[y]):
                        binary += '1' if image[dy][dx] == '#' else '0'
                    else:
                        binary += '1' if extrafill == '#' else '0'
            newimage[y].append(algo[int(binary, 2)])
    
    return newimage

# Part 1
newimage = process(process([[x for x in y] for y in image], '.'), '#')
print('\n'.join([''.join(x) for x in newimage]))
print(len(newimage), len(newimage[0]))
# Count pixels
print( sum([sum([1 if x == '#' else 0 for x in y]) for y in newimage]) )

# Part 2
newimage = image
for i in range(50):
    newimage = process(newimage, '#' if i % 2 else '.')
print( sum([sum([1 if x == '#' else 0 for x in y]) for y in newimage]) )