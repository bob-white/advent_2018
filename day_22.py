"""--- Day 22: Mode Maze ---

This is it, your final stop: the year -483. It's snowing and dark outside; the only light you can see is coming from a small cottage in the distance. You make your way there and knock on the door.

A portly man with a large, white beard answers the door and invites you inside. For someone living near the North Pole in -483, he must not get many visitors, but he doesn't act surprised to see you. Instead, he offers you some milk and cookies.

After talking for a while, he asks a favor of you. His friend hasn't come back in a few hours, and he's not sure where he is. Scanning the region briefly, you discover one life signal in a cave system nearby; his friend must have taken shelter there. The man asks if you can go there to retrieve his friend.

The cave is divided into square regions which are either dominantly rocky, narrow, or wet (called its type). Each region occupies exactly one coordinate in X,Y format where X and Y are integers and zero or greater. (Adjacent regions can be the same type.)

The scan (your puzzle input) is not very detailed: it only reveals the depth of the cave system and the coordinates of the target. However, it does not reveal the type of each region. The mouth of the cave is at 0,0.

The man explains that due to the unusual geology in the area, there is a method to determine any region's type based on its erosion level. The erosion level of a region can be determined from its geologic index. The geologic index can be determined using the first rule that applies from the list below:

    The region at 0,0 (the mouth of the cave) has a geologic index of 0.
    The region at the coordinates of the target has a geologic index of 0.
    If the region's Y coordinate is 0, the geologic index is its X coordinate times 16807.
    If the region's X coordinate is 0, the geologic index is its Y coordinate times 48271.
    Otherwise, the region's geologic index is the result of multiplying the erosion levels of the regions at X-1,Y and X,Y-1.

A region's erosion level is its geologic index plus the cave system's depth, all modulo 20183. Then:

    If the erosion level modulo 3 is 0, the region's type is rocky.
    If the erosion level modulo 3 is 1, the region's type is wet.
    If the erosion level modulo 3 is 2, the region's type is narrow.

For example, suppose the cave system's depth is 510 and the target's coordinates are 10,10. Using % to represent the modulo operator, the cavern would look as follows:

    At 0,0, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.
    At 1,0, because the Y coordinate is 0, the geologic index is 1 * 16807 = 16807. The erosion level is (16807 + 510) % 20183 = 17317. The type is 17317 % 3 = 1, wet.
    At 0,1, because the X coordinate is 0, the geologic index is 1 * 48271 = 48271. The erosion level is (48271 + 510) % 20183 = 8415. The type is 8415 % 3 = 0, rocky.
    At 1,1, neither coordinate is 0 and it is not the coordinate of the target, so the geologic index is the erosion level of 0,1 (8415) times the erosion level of 1,0 (17317), 8415 * 17317 = 145722555. The erosion level is (145722555 + 510) % 20183 = 1805. The type is 1805 % 3 = 2, narrow.
    At 10,10, because they are the target's coordinates, the geologic index is 0. The erosion level is (0 + 510) % 20183 = 510. The type is 510 % 3 = 0, rocky.

Drawing this same cave system with rocky as ., wet as =, narrow as |, the mouth as M, the target as T, with 0,0 in the top-left corner, X increasing to the right, and Y increasing downward, the top-left corner of the map looks like this:

M=.|=.|.|=.|=|=.
.|=|=|||..|.=...
.==|....||=..|==
=.|....|.==.|==.
=|..==...=.|==..
=||.=.=||=|=..|=
|.=.===|||..=..|
|..==||=.|==|===
.=..===..=|.|||.
.======|||=|=.|=
.===|=|===T===||
=|||...|==..|=.|
=.=|=.=..=.||==|
||=|=...|==.=|==
|=.=||===.|||===
||.|==.|.|.||=||

Before you go in, you should determine the risk level of the area. For the rectangle that has a top-left corner of region 0,0 and a bottom-right corner of the region containing the target, add up the risk level of each individual region: 0 for rocky regions, 1 for wet regions, and 2 for narrow regions.

In the cave system above, because the mouth is at 0,0 and the target is at 10,10, adding up the risk level of all regions with an X coordinate from 0 to 10 and a Y coordinate from 0 to 10, this total is 114.

What is the total risk level for the smallest rectangle that includes 0,0 and the target's coordinates?

"""

from itertools import product
from enum import IntEnum
from typing import Dict, Tuple, List

class Equipment(IntEnum):
    NEITHER = 0
    TORCH = 1
    CLIMB = 2

class Erosion(IntEnum):
    ROCKY = 0
    WET = 1
    NARROW = 2

def geo_index(p: complex) -> int:
    if p in geo_indices:
        return geo_indices[p]
    if p == target or 0 == p:
        return 0
    elif not p.real and p.imag:
        return int(p.imag) * 48271
    elif p.real and not p.imag:
        return int(p.real) * 16807
    return erosion(p-1) * erosion(p-1j)


def erosion(p: complex) -> int:
    if p in erosion_levels:
        return erosion_levels[p]
    geo_indices[p] = geo_index(p)
    erosion_levels[p] = ((geo_indices[p] + depth) % 20183)
    return erosion_levels[p]

def nearby(p: complex) -> Tuple[complex, complex, complex, complex]:
    return p + 1, p -1, p + 1j, p -1j

def check_nearby(p: complex, t: int, eq: Equipment, heap: List[Tuple[int, float, float, Equipment]]):
    for n in nearby(p):
        if n.real < 0 or n.imag < 0:
            continue
        if erosion(n) % 3 == eq:
            continue
        if (n, eq) in seen and seen[(n, eq)] <= t:
            continue
        seen[(n, eq)] = t
        heapq.heappush(heap, (t, n.real, n.imag, eq))

depth = 8103
target = 9 + 758j
# depth = 510
# target = 10 + 10j

erosion_levels: Dict[complex, int] = {}
geo_indices: Dict[complex, int] = {}
# Part 1
risk = 0
for x, y in product(range(int(target.real) + 1), range(int(target.imag) + 1)):
    p = x + 1j*y
    risk += erosion(p) % 3
print(risk)

# Part 2
import heapq
start = 0j
start_time = 0
seen = {(start, Equipment.TORCH): start_time}
# Tried this first with a list like I usually do, but it was way to slow.
# heapq guarantees that the item at index 0 is always the smallest, and uses some 
# c functions to ensure they are faster than me calling sort during each loop iteration.
heap: List[Tuple[int, float, float, Equipment]] = [(start_time, start.real, start.imag, Equipment.TORCH)]
heapq.heapify(heap)
while True:
    t, i, j, eq = heapq.heappop(heap)
    p = i + j * 1j
    if (p, eq) == (target, Equipment.TORCH):
        print(t)
        break
    
    t += 1
    check_nearby(p, t, eq, heap)

    t += 7
    er = erosion(p) % 3
    if eq == Equipment.TORCH:
        if er == Erosion.ROCKY:
            eq = Equipment.CLIMB
        elif er == Erosion.NARROW:
            eq = Equipment.NEITHER
    elif eq == Equipment.NEITHER:
        if er == Erosion.WET:
            eq = Equipment.CLIMB
        elif er == Erosion.NARROW:
            eq = Equipment.TORCH
    elif eq == Equipment.CLIMB:
        if er == Erosion.ROCKY:
            eq = Equipment.TORCH
        elif er == Erosion.WET:
            eq = Equipment.NEITHER

    check_nearby(p, t, eq, heap)