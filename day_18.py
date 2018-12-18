
from itertools import chain, product
from typing import Dict, Tuple, List
from collections import defaultdict

data = """
.#.#...|#.
.....#|##|
.|..|...#.
..|#.....#
#.#|||#|#|
...#.||...
.|....|...
||...#|.#|
|.||||..|.
...#.|..|.
""".split('\n')[1:-1]

with open('day_18.input', 'r') as f:
    data = f.read().split('\n')

def nearby(x, y):
    return [p for p in product(range(x-1, x+2), range(y-1, y+2)) if (x, y) != p]

def print_forest():
    c = '\n'.join(''.join(forest[(x, y)] for x in range(len(data[0]))) for y in range(len(data)))
    print(c)

def lumber_count():
    c = '\n'.join(''.join(forest[(x, y)] for x in range(len(data[0]))) for y in range(len(data)))
    return c.count('#') * c.count('|')

forest: Dict[Tuple[int, int], str] = {}
forest_graph:Dict[Tuple[int, int], List[Tuple[int, int]]] = defaultdict(list)
for y, line in enumerate(data):
    for x, c in enumerate(line):
        forest[(x, y)] = c

for x, y in product(range(len(data[0])), range(len(data))):
    forest_graph[(x, y)].extend(p for p in nearby(x, y) if p in forest)


def convert_area(x, y):
    surrounding = ''.join(forest[p] for p in forest_graph[(x, y)])
    spot = forest[(x, y)]
    if spot == '.' and surrounding.count('|') >= 3:
        return '|'
    elif spot == '|' and surrounding.count('#') >= 3:
        return '#'
    elif spot == '#':
        if surrounding.count('#') and surrounding.count('|'):
            return '#'
        return '.'
    return spot

# Tracking number of steps, and how large of a loop we're looking for.
# Each time we roll through the loop we check to see if we've seen the value before.
# If we haven't found a loop, we increase its size.
steps = 1000000000
current_step = 1
loop_size = 1
loop_remaining = loop_size
loop_val = forest.copy()
while current_step <= steps:
    current_step += 1
    new_forest = {}
    for x, y in product(range(len(data[0])), range(len(data))):
        new_forest[(x,y)] = convert_area(x, y)
    loop_remaining -= 1
    if not loop_remaining:
        if new_forest == loop_val:
            # Once we've found a loop, we can just math our out of the problem.
            # True divide the remaining steps by our loop size, then multiply that by the loop_size again
            # Add that to the current steps, and then we can just iterate the remaining
            current_step += ((steps - current_step) // loop_size) * loop_size
        else:
            loop_size += 1
            loop_val = new_forest
            loop_remaining = loop_size
    forest.update(new_forest)
    if current_step == 11:
        # Part 01
        print(lumber_count())

# Part 02
print(lumber_count())
