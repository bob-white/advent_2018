import itertools
from typing import Sequence

with open('day_01.input', 'r') as f:
    vals: Sequence[int] = list(map(int, f.readlines()))


def problem_01(input: Sequence[int]) -> int:
    return sum(input)

def problem_02(input: Sequence[int]) -> int:
    current: int = 0
    freq: set = {current}
    for val in itertools.cycle(vals):
        current += val
        if current in freq:
            break
        freq.add(current)
    return current

print(problem_01(vals))
print(problem_02(vals))
