from typing import Counter
from aocd import data

# data = """NNCB

# CH -> B
# HH -> N
# CB -> H
# NH -> C
# HB -> C
# HC -> B
# HN -> C
# NN -> C
# BH -> H
# NC -> B
# NB -> B
# BN -> B
# BB -> N
# BC -> B
# CC -> N
# CN -> C"""

(polymer, rules) = data.split('\n\n')

rules = {x[0:2]: x[6] for x in rules.splitlines()}

def do_step(chain):
    new_chain = ''
    last = ''
    for x in chain:
        if last:
            new_chain += rules[last + x]
        new_chain += x
        last = x
    return new_chain

chain = polymer
for x in range(10):
    chain = do_step(chain)

counts = {}
for x in chain:
    if x not in counts:
        counts[x] = 0
    counts[x] += 1
# print(chain, counts)
print(max(counts.values()) - min(counts.values()))

# Part 2

# Start at the end, and work backwards

# Build cache of after 10 for each
def do10(chain):
    for x in range(10):
        chain = do_step(chain)
    return chain

def get_counts(chain: str) -> Counter:
    counts = Counter()
    for x in chain:
        # if x not in counts:
        #     counts[x] = 0
        counts[x] += 1
    return counts

def combine_counts(chain: str, counts: dict[str, dict[str, int]]) -> dict[str, dict[str, int]]:
    # Init combined counts with initial chain
    comb_counts = get_counts(chain)
    # For each pair in chain
    last = ''
    for x in chain:
        if last:
            # Get counts
            this_count = get_counts(last + x)
            this_count[last] -= 1
            this_count[x] -= 1
            # Add to combined count
            comb_counts = {x: y + (this_count[x] or 0) for (x,y) in comb_counts}
        last = x
    return comb_counts


# Chain for each pair after 10
after10: dict[str, str] = {x: do10(x) for x in rules.keys()}

# Counts for each pair after 10, not including the pair itself
after10counts: dict[str, Counter] = {pair: get_counts(chain[1:-1]) for (pair,chain) in after10.items()}
print('a10c',after10counts)

# Counts for each pair after 20, not including the pair itself
# Take the chain after 10 for each pair
after20counts: dict[str, Counter] = dict()
for (pair, chain10) in after10.items():
    # For each chain, get the count of each pair, not including the pair itself (equivalent to another 10 steps)
    counts = after10counts[pair].copy()
    last = ''
    for x in chain10:
        if last:
            pair_count = after10counts[last + x]
            counts += pair_count
        last = x
    after20counts[pair] = counts
    
    # Add all the counts together, including the chain, and you have the count after 20 for each pair

print('after20counts', after20counts)

# After 30 steps
after30counts: dict[str, Counter] = dict()
# Take the chain after 10 for each pair
for (pair, chain10) in after10.items():
    # For each chain, get the count of each pair, not including the pair itself (equivalent to another 10 steps)
    counts = after10counts[pair].copy()
    last = ''
    for x in chain10:
        if last:
            pair_count = after20counts[last + x]
            counts += pair_count
        last = x
    after30counts[pair] = counts

print('after30counts', after30counts)

# After 40 steps
after40counts: dict[str, Counter] = dict()
# Take the chain after 10 for each pair
for (pair, chain10) in after10.items():
    # For each chain, get the count of each pair, not including the pair itself (equivalent to another 10 steps)
    counts = after10counts[pair].copy()
    last = ''
    for x in chain10:
        if last:
            pair_count = after30counts[last + x]
            counts += pair_count
        last = x
    after40counts[pair] = counts

print('after40counts', after40counts)

# Iterate the polymer, add the counts
counts = get_counts(polymer)
last = ''
for x in polymer:
    if last:
        counts += after40counts[last + x]
    last = x
print(counts)
print(max(counts.values()) - min(counts.values()))
