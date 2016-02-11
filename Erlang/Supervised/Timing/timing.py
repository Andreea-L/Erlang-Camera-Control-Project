import numpy as np

f = open("face_timing.time")
lines = f.readlines()

lines = np.delete(lines, slice(2, None, 3))
print zip(lines[::2], lines[1::2])
times = [int(j[6:-1])-int(i[6:-1]) for i,j in zip(lines[::2], lines[1::2])]
print times
print sum(times[i] for i in range(len(times)) if times[i] <= 999999)/(len(lines)*1000000.0)
