
import re
import time
from collections import defaultdict, Counter
from typing import Sequence, Optional, Dict

start_time = time.time()
with open('day_04.input', 'r') as f:
    vals: Sequence[str] = sorted(l[:-1] for l in f.readlines())

guards: Dict[int, list] = defaultdict(list)
guard_id = 0
for v in vals:
    if 'Guard' in v:
        guard_id = int(re.findall(r'\d+', v)[-1])
        guards[guard_id].append(v)
        continue
    guards[guard_id].append(v)


guard_minutes: Dict[int, list] = defaultdict(list)
asleep = 0
wakes = 0
for guard_id, schedule in guards.items():
    for action in schedule:
        d, t = re.findall(r'\[.*?\]', action)[0][1:-1].split()
        if 'falls asleep' in action:
            asleep = int(t.split(':')[-1])
        elif 'wakes up' in action:
            wakes = int(t.split(':')[-1])
            guard_minutes[guard_id].extend(range(asleep, wakes))

guard = max(guard_minutes.items(), key=lambda x: len(x[1]))[0]
minute = Counter(guard_minutes[guard]).most_common()[0][0]
print(minute * guard)

minute = 0
count = 0
guard = 0
for guard_id, minutes in guard_minutes.items():
    _minute, _count = Counter(minutes).most_common()[0]
    if _count > count:
        count = _count
        minute = _minute
        guard = guard_id

print(minute * guard)
