from xorshift import *
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import sympy as sm

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
    def __init__(self,X,Y,Z,W,mu,sig,step):
        self.pos = 0 #rd.gauss(mu,sig)
        self.random_gen = xor_shift_32(X,Y,Z,W)
        self.step = step

    def walk(self):
        if self.random_gen.random_value() > 0.5:
            self.pos += self.step
        else:
            self.pos -= self.step
    def get_pos(self):
        return self.pos



def run_random(title,savefile,T):
    #Add a list of walkers:
    N = 10000 # Number of walkers
    #T = 2 
    X = 10
    dt = 0.01
    dx = l = 0.01
    Tn = int(T/dt)
    print "Tn"
    walkers = []
    max_int = np.iinfo(np.uint32).max
    D = (dx**2/dt)*0.5
    sig = np.sqrt(((dx**2)*T)/dt)
    for i in range(N):
        X_rand = rd.randint(0,max_int)
        Y_rand = rd.randint(0,max_int)
        Z_rand = rd.randint(0,max_int)
        W_rand = rd.randint(0,max_int)
        walkers.append(walker(X_rand,Y_rand,Z_rand,W_rand,0,sig,dx))

    #Walk Tn steps
    for j in range(Tn):
        #print "j",j
        for walkeri in walkers:
            walkeri.walk()
    x = np.linspace(-X,X,2001)
    y = np.zeros(2001)
    width = 0.02
    sig_num = 0
    av_dis = 0
    for walkeri in walkers:
        y[(walkeri.get_pos()+10E-15+10)/dx] += 1
        if(walkeri.get_pos()> -sig) and (walkeri.get_pos()< sig):
            sig_num += 1
        av_dis += walkeri.get_pos()

    max_h = np.max(y)/float(N)
    plt.bar(x,y/float(N),width,align='center',label="random walk")
    def gauss(x,T):
        return 0.02*(1/np.sqrt(4*np.pi*D*T))*np.exp(-(x**2)/(4*D*T))

    plt.plot(x,gauss(x,T),'r',label="gauss function")
    #plt.plot(x,gauss(x,T*0.5),'g')
    plt.axis([-1,1,0,0.07])
    print "sig_num",sig_num
    print "average displacement", av_dis/float(N)

    plt.title(title)
    plt.legend()
    plt.savefig(savefile)
    plt.show()

#T_list = [2,8]
#for i in T_list:
#    run_random("time = %s" % i ,"plots/random_%s_t.png" % i ,i)
