from xorshift import *
import random as rd
import numpy as np
import matplotlib.pyplot as plt

X = 123456789
Y = 362436069
Z = 521288629
W = 88675123
#number = xor_shift(X,Y,Z,W)
#number = xor_shift_64(X,Y,W)
number32 = xor_shift_32(X,Y,Z,W)

#for i in range(20):
    #print "64",number.random_value()
    #print "32",number32.random_value()
def gauss_sig(x,sig):
    return (1/(sig*np.sqrt(2*np.pi)))*np.exp(-(x**2)/(2*sig**2))

class walker:
    def __init__(self,X,Y,Z,W,mu,sig):
        self.pos = 0 #rd.gauss(mu,sig)
        self.random_gen = xor_shift_32(X,Y,Z,W)
        self.step = 0.1

    def walk(self):

        if self.random_gen.random_value() > 0.5:
            self.pos += self.step
        else:
            self.pos -= self.step
    def get_pos(self):
        return self.pos


#Add a list of walkers:
N = 1000 # Number of walkers
T = 2 #
X = 10
dt = 0.1
dx = l = 0.1
Tn = int(T/dt)
print "Tn"
walkers = []
max_int = np.iinfo(np.uint32).max
D = 1
sig = np.sqrt(2*D*T)
for i in range(N):
    X_rand = rd.randint(0,max_int)
    Y_rand = rd.randint(0,max_int)
    Z_rand = rd.randint(0,max_int)
    W_rand = rd.randint(0,max_int)
    walkers.append(walker(X_rand,Y_rand,Z_rand,W_rand,0,sig))

#Walk Tn steps
for j in range(Tn):
    print "j",j
    for walker in walkers:
        walker.walk()
x = np.linspace(-X,X,201)
y = np.zeros(201)
width = 0.1
sig_num = 0
for walker in walkers:
    #print "walk",walker.get_pos()
    #print(walker.get_pos()+10)/dt
    y[(walker.get_pos()+10)/dt] += 1
    if(walker.get_pos()> -sig) and (walker.get_pos()< sig):
        sig_num += 1

max_h = np.max(y)/float(N)
plt.bar(x,y/float(N),width)
#plt.axis([-10,10,0,max_h*1.1])
def gauss(x,T):
    return (1/np.sqrt(4*np.pi*D*T))*np.exp(-(x**2)/(4*D*T))

plt.plot(x,gauss(x,T))
print "sig_num",sig_num

plt.show()
