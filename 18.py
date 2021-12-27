from aocd import lines
from ast import literal_eval
from typing import Union
from math import ceil, floor

sfnum = tuple[Union[int, 'sfnum'], Union[int, 'sfnum']]

data: list[sfnum] = [literal_eval(x) for x in lines]

def reduce(num: sfnum):
    did = True
    while did:
        (num, _, _, did) = explode(num)
        # if did: print('After explode', num)
        if not did:
            (num, did) = split(num)
            # if did: print('After split', num)
    return num

def addleft(num: sfnum, toadd: int) -> sfnum:
    if toadd == 0:
        return num
    if type(num) is int:
        return num + toadd
    return [addleft(num[0], toadd), num[1]]

def addright(num: sfnum, toadd: int) -> sfnum:
    if toadd == 0:
        return num
    if type(num) is int:
        return num + toadd
    return [num[0], addright(num[1], toadd)]

def explode(num: sfnum, level: int = 1) -> tuple[sfnum, int, int, bool]: # sfnum, passleft, passright
    if type(num) is int:
        return (num, 0, 0, False)
    if level == 4:
        if type(num[0]) is list:
            # Explode left
            return ([0, addleft(num[1], num[0][1])], num[0][0], 0, True)
        if type(num[1]) is list:
            return ([addright(num[0], num[1][0]), 0], 0, num[1][1], True)
        return (num, 0, 0, False)
    else:
        if type(num[0]) is list:
            (newleft, passleft, passright, did) = explode(num[0], level + 1)
            if did: # Exploded
                return ([newleft, addleft(num[1], passright)], passleft, 0, did)
        if type(num[1]) is list:
            (newright, passleft, passright, did) = explode(num[1], level + 1)
            if did:
                return ([addright(num[0], passleft), newright], 0, passright, did)
        return (num, 0, 0, False)

def split(num: sfnum) -> tuple[sfnum, bool]:
    if type(num) is list:
        (left, right) = num
        (left, did) = split(left)
        if not did:
            (right, did) = split(right)
        return ([left, right], did)
    if num < 10:
        return (num, False)
    return ([floor(num/2), ceil(num/2)], True)

def add(num1: sfnum, num2: sfnum):
    res = [num1, num2]
    # print('After addition', res)
    return reduce(res)

def magnitude(num: sfnum) -> int:
    if type(num) is int:
        return num
    return magnitude(num[0])*3 + magnitude(num[1])*2

# print(add([[[[4,3],4],4],[7,[[8,4],9]]],[1,1]))

total = data[0]
for sfnum in data[1:]:
    total = add(total, sfnum)
print(magnitude(total))

# Part 2
largest = 0
for x in data:
    for y in data:
        if x != y:
            mag = magnitude(add(x, y))
            largest = max(largest, mag)
print(largest)