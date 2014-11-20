from xorshift import *

X = 123456789
Y = 362436069
Z = 521288629
W = 88675123
#number = xor_shift(X,Y,Z,W)
#number = xor_shift_64(X,Y,W)
number32 = xor_shift_32(X,Y,Z,W)

for i in range(20):
    #print "64",number.random_value()
    print "32",number32.random_value()

class walker:
    def __init__(self,X,Y,Z,W):
        self.pos = 0
        self.random_gen = xor_shift_32(X,Y,Z,W)

    def walk(self):
        if gen.random_value >

