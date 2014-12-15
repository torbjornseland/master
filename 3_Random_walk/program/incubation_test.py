import random as rd
import numpy as np

N = 100000
time_steps = 100

lis = np.ones(N)
all_val = 0
round_val = 0
total = 0
round_count = 0

while all_val != N:
    round_count += 1
    for i in range(N):
        if lis[i] == 1:
            ra = rd.random()
            if(ra < 0.0044036):
                lis[i] = 0
                all_val += 1
                round_val += 1
    print "round:",round_count,"val:",round_val
    total += round_val*(round_count)
    round_val = 0

print total/float(N*time_steps)


