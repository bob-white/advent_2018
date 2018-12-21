
from collections import deque, defaultdict
from pprint import pprint
from typing import Dict, List, Tuple, Sequence, Set
data = '^ENNWSWW(NEWS|)SSSEEN(WNSE|)EE(SWEN|)NNN$'[1:-1]
data = '^ESSWWN(E|NNENN(EESS(WNSE|)SSS|WWWSSSSE(SW|NNNE)))$'[1:-1]
data = '^WSSEESWWWNW(S|NENNEEEENN(ESSSSW(NWSW|SSEN)|WSWWN(E|WWS(E|SS))))$'
directions = {'N': 1, 'S': -1, 'W': -1j, 'E': 1j}

with open('day_20.input') as f:
    data = f.read()[1:-1]

graph: Dict[complex, List[complex]] = defaultdict(list)
stack: List[complex] = []
p: complex = 0
for c in data:
    if c in directions:
        d = directions[c]
        graph[p].append(d+p)
        p += d
    elif c in '(':
        # starting a new group, we want to store this position so we can come back to it.
        stack.append(p)
    elif c in '|':
        # We've hit a branch, we need to roll back to the group start.
        p = stack[-1]
    elif c in ')':
        # Closing out the group, removing the last start point.
        stack.pop()

def solve():
    queue = deque([(0, 0)])
    seen = set()
    distances = {}
    over_1k = 0
    while queue:
        p, d = queue.pop()
        if p in seen:
            continue
        seen.add(p)
        distances[p] = d
        if d >= 1000:
            over_1k +=1
        for n in graph[p]:
            queue.append((n, d+1))

    print(max(distances.values()))
    print(over_1k)

solve()