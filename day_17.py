from itertools import product, count
from collections import deque, defaultdict
from typing import Tuple, List, Set, Dict

data = """
x=495, y=2..7
y=7, x=495..501
x=501, y=3..7
x=498, y=2..4
x=506, y=1..2
x=498, y=10..13
x=504, y=10..13
y=13, x=498..504
""".split('\n')[1:-1]

with open('day_17.input', 'r') as f:
    data = f.read().split('\n')

def get_bounds(cavern):
    x, y = zip(*cavern)
    return min(x)-2, max(x)+2, min(y)-1, max(y)+1

def print_cavern(cavern):
    l, r, _, h = get_bounds(cavern)
    c = '\n'.join(''.join(cavern.get((x, y), '.') for x in range(l, r)) for y in range(0, h))
    if len(c) >= 10000:
        with open('tmp', 'w') as f:
            f.write(c)
    else:
        print(c)
        print()

def build_cavern():
    cavern = {}
    for line in data:
        a, b = line.split(', ')
        if a.startswith('x='):
            x = [int(a[2:])] * 2
            y = list(map(int, b[2:].split('..')))
        else:
            y = [int(a[2:])] * 2
            x = list(map(int, b[2:].split('..')))
        x[1] += 1
        y[1] += 1
        for i, j in product(range(*x), range(*y)):
            cavern[(i, j)] = '#'
    return cavern


def depth_test(cavern, x, y) -> Tuple[int, int]:
    for i in count(y+1):
        if (x, i) in cavern:
            return (x, i-1)
    return (x, -1)


def next_move(cavern, x, y) -> List[Tuple[int, int]]:
    down = (x, y+1)
    if down not in cavern or cavern[down] == '|':
        return [down]
    left, right = ((x-1, y), (x+1, y))
    return [p for p in (left, right) if p not in cavern]

cavern = build_cavern()
water_count = list(cavern.values()).count('~') + list(cavern.values()).count('|')
seen: Set[Tuple[int, int]] = set()
l, r, top, bottom = get_bounds(cavern)
start = [(500, top)]
counter = 0
while counter <= 10:
    queue = deque(start)
    water: Dict[int, List[int]] = defaultdict(list)
    while queue:
        x, y = queue.popleft()
        if (x, y) in seen:
            continue
        seen.add((x,y ))
        water[y].append(x)
        for x2, y2 in next_move(cavern, x, y):
            if l < x2 < r and y2 < bottom:
                queue.append((x2, y2))
                cavern[(x2, y2)] = '|'

    for depth in water:
        groups = []
        group = []
        vals = sorted(water[depth], reverse=True)
        s = vals.pop()
        group.append(s)
        groups.append(group)
        while vals:
            n = vals.pop()
            if (n - s) > 1:
                group = []
                groups.append(group)
            group.append(n)
            s = n
        for group in groups:
            if not any(next_move(cavern, x, depth) for x in group):
                for x in group:
                    cavern[(x, depth)] = '~'
                    seen.discard((x, depth))
    for x, y in seen:
        if cavern.get((x-1, y)) == cavern.get((x+1, y)) == '#' and cavern.get((x, y+1)) == '~':
            cavern[(x, y)] = '~'

    tilde = list(cavern.values()).count('~')
    pipes = list(cavern.values()).count('|')
    new_count = tilde + pipes
    # print_cavern(cavern)
    if new_count == water_count or not seen:
        counter += 1
    else:
        water_count = new_count
        for item in seen:
            if cavern.get(item) == '|':
                cavern.pop(item)
        seen.clear()

# print_cavern(cavern)
print(water_count)
print(tilde)
