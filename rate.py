import fileinput
import sys
import statistics

max_samples = 10
if len(sys.argv) > 1:
    max_samples = int(sys.argv[1])

sz = []
for line in fileinput.input():
    sz.append(int(line.split()[0]))
    if len(sz) > max_samples:
        sz.pop(0)
    print(f"aa {statistics.mean(sz)/1000000} zz")
