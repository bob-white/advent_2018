import re
from collections import defaultdict, Counter
from itertools import product, chain, combinations
from math import log, floor
from heapq import heappush, heappop
from typing import List, Dict, Tuple, Set, Sequence, Any

Point = Sequence[int]
BoundingBox = Tuple[Tuple[int, int, int], Tuple[int, int, int]]

def distance(start: Point, end: Point) -> int:
    x, y, z = start
    i, j, k = end
    return abs(x-i) + abs(y-j) + abs(z-k)


def get_exteme_bounds(bots: List[Point]):
    """
    Gets the extreme bounding box for the nanobots.
    The extreme bounding box includes the radius of the bot, not just their positions.
    """
    extremes = [[i + bot[3] for i in bot[:3]] for bot in bots]
    x, y, z = zip(*extremes)
    return (min(x), min(y), min(z)), (max(x), max(y), max(z))

def get_start_box_size(bots: List[Point]) -> int:
    extreme_max = max(chain.from_iterable(get_exteme_bounds(bots)))
    return 2**(floor(log(extreme_max, 2)) + 1)

def bot_intersects_box(bot: Sequence[int], box: BoundingBox) -> bool:
    """Check to see if a given nanobot's range intersects with a bounding box.
    
    Arguments:
        bot {Sequence[int]}
        box {BoundingBox}
    
    Returns:
        bool
    """

    *pnt, r = bot
    dist = 0
    box_min_max = zip(*box)
    for (box_min, box_max), i in zip(box_min_max, pnt):
        box_max -= 1
        dist -= box_max - box_min
        dist += abs(i-box_min)
        dist += abs(i-box_max)
    dist //= 2
    return dist <= r


def num_intersections(box) -> int:
    return sum(bot_intersects_box(bot, box) for bot in bots)


data = """pos=<0,0,0>, r=4
pos=<1,0,0>, r=1
pos=<4,0,0>, r=3
pos=<0,2,0>, r=1
pos=<0,5,0>, r=3
pos=<0,0,3>, r=1
pos=<1,1,1>, r=1
pos=<1,1,2>, r=1
pos=<1,3,1>, r=1""".split('\n')
with open('day_23.input', 'r') as f:
    data = f.read().split('\n')

bots: List[Sequence[int]] = [list(map(int, re.findall(r'-?\d+', line))) for line in data]

*point, radius = max(bots, key=lambda x: x[-1])
# Part 1
print(sum(distance(point, p[:3]) <= radius for p in bots))


size = get_start_box_size(bots)
boxes = [((-size, -size, -size), (size, size, size))]
# So heaps always put the smallest item at the 0 index, so we need to negate the elements we care about
# and our goal it sort by the maximum number of intersections, then the box size, so we can ignore large empty boxes.
# After that we care about distance to origin, we wnat the smallest one of those so we don't negate.
heap: List[Any] = [(-num_intersections(boxes[0]), -2*size, -3*size, boxes[0])]
c: Dict[int, int] = defaultdict(int)
while heap:
    neg_intersections, neg_size, dist_to_origin, box = heappop(heap)
    if neg_size == -1:
        print('')
        print(dist_to_origin)
        break
    new_size = neg_size // -2 # We're carving the box into 8 new ones.
    for octant in product(range(2), range(2), range(2)):
        new_min = tuple(b + new_size * o for b, o in zip(box[0], octant))
        new_max = tuple(b + new_size for b in new_min)
        new_box = (new_min, new_max)
        new_intersections = num_intersections(new_box)
        heappush(heap, (-new_intersections, -new_size, distance(new_min, [0, 0, 0]), new_box))
        c[new_size] += 1
