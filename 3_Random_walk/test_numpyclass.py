import numpy as np
from xorshift import *

class walker(np.ndarray):
    
    def __new__(cls,*args,**kwargs):
        print 'In __new__ with class %s' % cls
        return np.ndarray.__new__(cls, *args, **kwargs)

    def __init__(self, *args, **kwargs):
        # in practice you probably will not need or want an __init__
        # method for your subclass
        self.pos = 0
        self.random_gen = xor_shift_32(args[0])
        self.step = 0.1
        print 'In __init__ with class %s' % self.__class__
    
    def walk(self):

        if self.random_gen.random_value() > 0.5:
            self.pos += self.step
        else:
            self.pos += self.step
    
    def get_pos(self):
        print "test"
        return self.pos



walk = walker((4,2,1,2))
print "pos=",walk.get_pos()
a = np.arange(10)
cast_a = a.view(walker)
print type(cast_a)
print cast_a.get_pos()
#for i in cast_a:
#    i = walker((1,2,3,4))

#print cast_a[:].get_pos()


"""    
    def __init__(self,X,Y,Z,W):
        self.pos = 0
        self.random_gen = xor_shift_32(X,Y,Z,W)
        self.step = 0.1
"""
