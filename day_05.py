
import re
import time
import string

start_time = time.time()
with open('day_05.input', 'r') as f:
    poly = f.read()
pairs = [''.join(pair) for pair in zip(string.ascii_lowercase, string.ascii_uppercase)]
pairs.extend(p[::-1] for p in pairs[:])

def collapse_poly(poly):
    while any(p in poly for p in pairs):
        for p in pairs:
            poly = poly.replace(p, '')
    return poly

poly = collapse_poly(poly)
print(len(poly))
counts = []
for l, u in zip(string.ascii_lowercase, string.ascii_uppercase):
    new_poly = poly.replace(u, '').replace(l, '')
    counts.append(len(collapse_poly(new_poly)))    

print(min(counts))
