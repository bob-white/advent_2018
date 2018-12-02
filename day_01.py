import itertools

with open('day_01.input', 'r' ) as f:
    vals = list(map(int, f.readlines()))

current = 0
freq = { current }
for val in itertools.cycle(vals):
    current += val
    if current in freq:
        break
    freq.add(current)

print(sum(vals))
print(current)