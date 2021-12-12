from aocd import lines
from statistics import median

scores = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}

pairs = {
    '(':')',
    '[':']',
    '{':'}',
    '<':'>'
}

def get_score(line):
    stack = []
    for x in line:
        if x in '([{<':
            stack.append(x)
        else:
            top = stack.pop()
            if x != pairs[top]:
                return scores[x]
    return 0

print(sum([get_score(x) for x in lines]))

part2score = {    
    ')': 1,
    ']': 2,
    '}': 3,
    '>': 4
}

def part2(line):
    stack = []
    for x in line:
        if x in '([{<':
            stack.append(x)
        else:
            top = stack.pop()
            if x != pairs[top]:
                return None

    score = 0
    stack.reverse()
    for opening in stack:
        score *= 5
        score += part2score[pairs[opening]]
    return score

print(median([part2(x) for x in lines if part2(x)]))