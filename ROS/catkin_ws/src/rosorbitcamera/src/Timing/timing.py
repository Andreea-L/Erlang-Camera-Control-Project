import numpy as np

f = open("worker_timing.time")
lines = f.readlines()

lines = np.delete(lines, slice(2, None, 3))
print zip(lines[::2], lines[1::2])
times = [int(j)-int(i) for i,j in zip(lines[::2], lines[1::2])]
print times
print sum(times)/len(times)
