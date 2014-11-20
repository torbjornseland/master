import numpy as np

class xor_shift():
    def __init__(self,X,Y,Z,W):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W

    def random_value(self):
        t = self.X ^ (self.X << 15)
        self.X = self.Y
        self.Y = self.Z
        self.Z = self.W
        self.W = self.W ^ (self.W >> 21) ^ t ^ (t >> 4)
        return self.W

class xor_shift_32():
    def __init__(self,X,Y,Z,W):
        self.X = np.uint32(X)
        self.Y = np.uint32(Y)
        self.Z = np.uint32(Z)
        self.W = np.uint32(W)
        self.max_int = np.iinfo(np.uint32).max
        self.t = np.uint32(0)

    def random_value(self):
        self.t = self.X ^ (self.X << 15)
        self.X = np.uint32(self.Y)
        self.Y = np.uint32(self.Z)
        self.Z = np.uint32(self.W)
        self.W = np.uint32(self.W ^ (self.W >> 21) ^ self.t ^ (self.t >> 4))
        return self.W/float(self.max_int)
#W1 = xor_shift() # 252977563114
#W2 = xor_shift() # 646616338854
#W3 = xor_shift() # 476657867818

#print W1
#print W2
#print W3
