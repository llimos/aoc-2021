from aocd import lines

# lines = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
# edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
# fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
# fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
# aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
# fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
# dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
# bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
# egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
# gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce""".splitlines()

def uniques(code):
    return len([x for x in code.split(' ') if len(x) in (2,3,4,7)])

print(sum([uniques(x.split(' | ')[1]) for x in lines]))

# Part 2

def getvalue(line):
    (codes, output) = line.split(' | ')
    codes = [{c for c in x} for x in codes.split(' ')]

    solved = {}

    # Split by count
    bycount = {x:[c for c in codes if len(c) == x] for x in (2,3,4,5,6,7)}

    # Find the code corresponding to 1, 4, 7, 8 (all unique)
    solved[1] = one = bycount[2][0]
    solved[4] = four = bycount[4][0]
    solved[7] = seven = bycount[3][0]
    solved[8] = eight = bycount[7][0]

    # Segment c + f are in 1
    cf = solved[1]
    # Segment a is the one in 7 but not 1
    a = solved[7].difference(solved[1])
    # Segment b + d are in 4 but not 1
    bd = solved[4].difference(solved[1])

    # 6 segments: 0, 9, 6
    # The one that doesn't have both b + d is 0
    solved[0] = zero = [x for x in bycount[6] if not x.issuperset(bd)][0]
    assert(len([x for x in bycount[6] if not x.issuperset(bd)])==1)
    # The one that has c + f and is not 0 is 9
    solved[9] = nine = [x for x in bycount[6] if x.issuperset(cf) and x != solved[0]][0]
    assert(len([x for x in bycount[6] if x.issuperset(cf) and x != solved[0]])==1)
    # The other is 6
    solved[6] = six = [x for x in bycount[6] if x != solved[0] and x != solved[9]][0]
    assert(len([x for x in bycount[6] if x != solved[0] and x != solved[9]])==1)

    # 5 segments: 2, 3, 5
    # The one that has c + f is 3
    solved[3] = three = [x for x in bycount[5] if x.issuperset(cf)][0]
    # The one that doesn't have b + d and is not 3 is 2
    solved[2] = two = [x for x in bycount[5] if not x.issuperset(bd) and x != solved[3]][0]
    # The other is 5
    solved[5] = five = [x for x in bycount[5] if x != solved[3] and x != solved[2]][0]

    output = [{c for c in x} for x in output.split(' ')]
    
    results = [[n for (n,c) in solved.items() if c == x][0] for x in output]
    results.reverse()
    return sum([x * (10**i) for (i,x) in enumerate(results)])



print(sum([getvalue(x) for x in lines]))