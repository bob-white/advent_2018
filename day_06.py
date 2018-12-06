
from itertools import product
from collections import defaultdict
from typing import List, Tuple, Dict
with open('day_06.input', 'r') as f:
    data = f.read()

points = [tuple(map(int, l.split(', '))) for l in data.split('\n')]

x_min, *_, x_max = sorted(p[0] for p in points)
y_min, *_, y_max = sorted(p[1] for p in points)

area: Dict[int, int] = defaultdict(int)

def _distance(p, q):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def get_closest(point: Tuple[int, int], points: List[tuple]) -> int:
    closest = sorted([(idx, _distance(point, _point)) for idx, _point in enumerate(points)], key=lambda x: x[1])
    if closest[0][1] == closest[1][1]:
        return -1
    return closest[0][0]

for p in product(range(x_min, x_max), range(y_min, y_max)):
    closest = get_closest(p, points)
    x, y = p
    if -1 in (closest, area[closest]):
        continue
    elif x in (x_min, x_max) or y in (y_min, y_max):
        area[closest] = -1
    else:
        area[closest] += 1

print(max(area.values()))

safe = 0
for p in product(range(x_min, x_max), range(y_min, y_max)):
    total_distance = sum(_distance(p, point) for point in points)
    if total_distance < 10000:
        safe += 1

print(safe)


