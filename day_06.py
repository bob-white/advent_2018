"""--- Day 6: Chronal Coordinates ---

The device on your wrist beeps several times, and once again you feel like you're falling.

"Situation critical," the device announces. "Destination indeterminate. Chronal interference detected. Please specify new target coordinates."

The device then produces a list of coordinates (your puzzle input). Are they places it thinks are safe or dangerous? It recommends you check manual page 729. The Elves did not give you a manual.

If they're dangerous, maybe you can minimize the danger by finding the coordinate that gives the largest distance from the other points.

Using only the Manhattan distance, determine the area around each coordinate by counting the number of integer X,Y locations that are closest to that coordinate (and aren't tied in distance to any other coordinate).

Your goal is to find the size of the largest area that isn't infinite. For example, consider the following list of coordinates:

1, 1
1, 6
8, 3
3, 4
5, 5
8, 9

If we name these coordinates A through F, we can draw them on a grid, putting 0,0 at the top left:

..........
.A........
..........
........C.
...D......
.....E....
.B........
..........
..........
........F.

This view is partial - the actual grid extends infinitely in all directions. Using the Manhattan distance, each location's closest coordinate can be determined, shown here in lowercase:

aaaaa.cccc
aAaaa.cccc
aaaddecccc
aadddeccCc
..dDdeeccc
bb.deEeecc
bBb.eeee..
bbb.eeefff
bbb.eeffff
bbb.ffffFf

Locations shown as . are equally far from two or more coordinates, and so they don't count as being closest to any.

In this example, the areas of coordinates A, B, C, and F are infinite - while not shown here, their areas extend forever outside the visible grid. However, the areas of coordinates D and E are finite: D is closest to 9 locations, and E is closest to 17 (both including the coordinate's location itself). Therefore, in this example, the size of the largest area is 17.

What is the size of the largest area that isn't infinite?

Your puzzle answer was 3722.
--- Part Two ---

On the other hand, if the coordinates are safe, maybe the best you can do is try to find a region near as many coordinates as possible.

For example, suppose you want the sum of the Manhattan distance to all of the coordinates to be less than 32. For each location, add up the distances to all of the given coordinates; if the total of those distances is less than 32, that location is within the desired region. Using the same coordinates as above, the resulting region looks like this:

..........
.A........
..........
...###..C.
..#D###...
..###E#...
.B.###....
..........
..........
........F.

In particular, consider the highlighted location 4,3 located at the top middle of the region. Its calculation is as follows, where abs() is the absolute value function:

    Distance to coordinate A: abs(4-1) + abs(3-1) =  5
    Distance to coordinate B: abs(4-1) + abs(3-6) =  6
    Distance to coordinate C: abs(4-8) + abs(3-3) =  4
    Distance to coordinate D: abs(4-3) + abs(3-4) =  2
    Distance to coordinate E: abs(4-5) + abs(3-5) =  3
    Distance to coordinate F: abs(4-8) + abs(3-9) = 10
    Total distance: 5 + 6 + 4 + 2 + 3 + 10 = 30

Because the total distance to all coordinates (30) is less than 32, the location is within the region.

This region, which also includes coordinates D and E, has a total size of 16.

Your actual region will need to be much larger than this example, though, instead including all locations with a total distance of less than 10000.

What is the size of the region containing all locations which have a total distance to all given coordinates of less than 10000?

Your puzzle answer was 44634.

"""

import time
from itertools import product
from collections import defaultdict
from typing import List, Tuple, Dict, Sequence, cast, Union
with open('day_06.input', 'r') as f:
    data = f.read()

Point = Tuple[int, int]
Rect = Tuple[int, int, int, int]

points: Sequence[Point] 
points = cast(Sequence[Point], [tuple(map(int, l.split(', '))) for l in data.split('\n')])

x_min, *_, x_max = sorted(p[0] for p in points)
y_min, *_, y_max = sorted(p[1] for p in points)


def manhattan_distance(p: Point, q: Point) -> int:
    """Returns the Manhattan distance between two points
    
    https://en.wiktionary.org/wiki/Manhattan_distance

    Arguments:
        p {Point} -- Start point
        q {Point} -- End Point
    
    Returns:
        {int} -- distance.
    """

    return abs(p[0] - q[0]) + abs(p[1] - q[1])

def get_closest(point: Point, points: Sequence[Point]) -> int:
    """Calculates the closest point to the given point from a sequence of points.
    Returns -1 if there is a tie for the closet point.
    
    Arguments:
        point {Point} -- The given point.
        points {Sequence[Point]} -- The points to check against.
    
    Returns:
        int -- The closest point, or -1 in case of a tie.
    """

    closest = sorted(((idx, manhattan_distance(point, _point)) for idx, _point in enumerate(points)), key=lambda x: x[1])
    if closest[0][1] == closest[1][1]:
        return -1
    return closest[0][0]

def get_largest_area(rect: Rect, points: Sequence[Point]) -> int:
    """Find the largest bounded area around all the points.

    This basically is creating a voronai using the manhattan distance, and throwing out any ties.
    If any of the cells are on the edge of the diagram, we declare their area to be infinite, and 
    so we just ignore those.
    
    Arguments:
        rect {Rect} -- The diagram size
        points {Sequence[Point]} -- The points to cluster around.
    
    Returns:
        int -- The size of the largest bounded cluster.
    """

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

def get_safe_area(rect: Rect, points: Sequence[Point], safe_range: int = 10000) -> int:
    """This computes the size of the safe landing zone.
    The safe area is defined by any point that has a total distance to all of hte points less
    than the given `safe_range`
    Arguments:
        rect {Rect} -- The size of the diagram.
        points {Sequence[Point]} -- The series of points to check against.
    
    Keyword Arguments:
        safe_range {int} -- The max total distance to all points considered safe. (default: {10000})
    
    Returns:
        int -- The size of the safe zone's area.
    """

    x_max, y_max, x_min, y_min = rect
    safe = 0
    for p in product(range(x_min, x_max), range(y_min, y_max)):
        total_distance = sum(manhattan_distance(p, point) for point in points)
        if total_distance < safe_range:
            safe += 1
    return safe


print(get_largest_area((x_max, y_max, x_min, y_min), points))
print(get_safe_area((x_max, y_max, x_min, y_min), points))
