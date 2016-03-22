import numpy as np

f = open("main_timing.time")
lines = f.readlines()

lines = np.delete(lines, slice(1, None, 2))
times = []
for i in range(1, len(lines)):
   times.append(int(lines[i]) - int(lines[i-1]))
print times
print sum(times)/len(times)
