import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys

plotname = "plot_data/test"

Nx = 50
N = 80

L = 60
T = 20

#List of values


x = np.linspace(-L,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1) #Picard

"""
q = 1
s = -2/float(q)
k = q/float(np.sqrt(2*(q+2)))
c = (q+4)/float(np.sqrt(2*q+4))
alpha = 1
def exact_u(x,t):
    return (1+alpha*np.exp(k*(x-c*t)))**s
"""

q = 1
s = 2/float(q)
k = q/float(np.sqrt(2*(q+2)))
c = (q+4)/float(np.sqrt(2*q+4))
alpha = 1
def reverse_exact_u(x,t):
    return 1/((1+alpha*np.exp(k*(x-c*t)))**s)




for n in range(0, N):
    for i in range(3):
        alpha = (i+1)*100
        u[:] = reverse_exact_u(x,t[n])
        plt.plot(x,u)
    plt.axis([-60,60,-0.2,1.2])
    plt.savefig("plot_data/tmp%04d.png" % (n/1))
    plt.close()


os.system('avconv -r 10 -i %s -vcodec mpeg4 %s' %('plot_data/tmp%04d.png','testfile.mp4'))

for filename in glob.glob('plot_data/tmp*.png'):
	os.remove(filename)

os.system('vlc testfile.mp4')
os.remove('testfile.mp4')
