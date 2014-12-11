import random as rd
import numpy as np


lis = np.ones(1000)
all_val = 0
round_val = 0
total = 0
round_count = 0

while all_val != 1000:
    round_count += 1
    for i in range(1000):
        if lis[i] == 1:
            ra = rd.random()
            if(ra < 0.0137):
                lis[i] = 0
                all_val += 1
                round_val += 1
    print "round:",round_count,"val:",round_val
    total += round_val*(round_count)
    round_val = 0

print total/float(1000*100)


