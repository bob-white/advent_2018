
import time
from itertools import product
from collections import defaultdict
from typing import List, Tuple, Dict, Sequence, cast
with open('day_06.input', 'r') as f:
    data = f.read()

Point = Tuple[int, int]
Rect = Tuple[int, int, int, int]

points: Sequence[Point] 
points = cast(Sequence[Point], [tuple(map(int, l.split(', '))) for l in data.split('\n')])

x_min, *_, x_max = sorted(p[0] for p in points)
y_min, *_, y_max = sorted(p[1] for p in points)


def _distance(p: Point, q: Point):
    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def get_closest(point: Point, points: Sequence[Point]) -> int:
    closest = sorted(((idx, _distance(point, _point)) for idx, _point in enumerate(points)), key=lambda x: x[1])
    if closest[0][1] == closest[1][1]:
        return -1
    return closest[0][0]

def get_largest_area(rect: Rect, points: Sequence[Point]) -> int:
    area: Dict[int, int] = defaultdict(int)
    x_max, y_max, x_min, y_min = rect
    for x, y in product(range(x_min, x_max), range(y_min, y_max)):
        closest = get_closest((x, y), points)
        if -1 in (closest, area[closest]):
            continue
        elif x in (x_min, x_max) or y in (y_min, y_max):
            area[closest] = -1
        else:
            area[closest] += 1
    return max(area.values())

def get_safe_area(rect: Rect, points: Sequence[Point]) -> int:
    safe = 0
    for p in product(range(x_min, x_max), range(y_min, y_max)):
        total_distance = sum(_distance(p, point) for point in points)
        if total_distance < 10000:
            safe += 1
    return safe

def compute_distances(rect: Rect, points: Sequence[Point]) -> Dict[Point, List[Tuple[int, int]]]:
    distances: Dict[Point, List[Tuple[int, int]]] = defaultdict(list)
    x_max, y_max, x_min, y_min = rect
    for x, y in product(range(x_min, x_max), range(y_min, y_max)):
        for idx, point in enumerate(points):
            if x in (x_min, x_max) or y in (y_min, y_max):
                distance = -1
            else:
                distance = _distance((x, y), point)
            distances[(x, y)].append((idx, distance))
    return distances

start = time.time()
print(get_largest_area((x_max, y_max, x_min, y_min), points))
print(time.time() - start)
start = time.time()
print(get_safe_area((x_max, y_max, x_min, y_min), points))
print(time.time() - start)
