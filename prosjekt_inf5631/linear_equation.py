import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob

Nx = 2000
N = 50

L = 2
T = 2

beta_0 = 1
r = 1

x = np.linspace(0,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)

C = (beta_0*dt)/(2*dx**2)
D = dt*r*0.5

def I(x):
	return (1-(x-1)**2)
"""
def I(x):
	if(x >= 0.9 and x <= 1.1):
		return 1
	else:
		return 0
"""
# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)

for i in range(1,Nx):
	A[i,i-1] = -C	
	A[i,i+1] = -C	
	A[i,i] = 1+2*C-D

A[0,0] = A[Nx,Nx] = 1

#Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
	u_1[i] = I(x[i])

	
for n in range(0, N):
	#Compute b and solve linear system
	for i in range(1, Nx):
		b[i] = (1-2*C+D)*u_1[i]+C*(u_1[i-1]+u_1[i+1])
	b[0] = b[Nx] = 0
	u[:] = sl.solve(A, b)
	

	plt.plot(x,u)
	plt.axis([0,2,-1,1])
	plt.savefig("tmp%04d.png" % n)
	plt.close()
	
	#Update u_1 before next step
	u_1[:] = u




os.system('avconv -r 10 -i %s -vcodec mpeg4 %s' %('tmp%04d.png','testfile.mp4'))

for filename in glob.glob('tmp*.png'):
	os.remove(filename)

os.system('vlc testfile.mp4')
os.remove('testfile.mp4')
