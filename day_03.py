
import re
from collections import defaultdict
from typing import Sequence, Optional, Dict

with open('day_03.input', 'r') as f:
    vals: Sequence[str] = list(f.readlines())

fabric: Dict[tuple, int] = defaultdict(int)
rects: Dict[int, tuple] = {}


def part_01(vals: Sequence[str]) -> int:
    for line in vals:
        idx, x, y, w, h = map(int, re.findall(r'\d+', line))
        rects[idx] = x, y, w, h
        for i in range(w):
            for j in range(h):
                fabric[((x+i), (y+j))] += 1
    return sum(i >= 2 for i in fabric.values())


def part_02(vals: Sequence[str]) -> Optional[int]:
    for idx, (x, y, w, h) in rects.items():
        if all(fabric[(x+i), (y+j)] == 1 for i in range(w) for j in range(h)):
            return idx
    return None


print(part_01(vals))
print(part_02(vals))
