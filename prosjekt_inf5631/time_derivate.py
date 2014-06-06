import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys

Nx = 2000
N = 50

L = 2
T = 20


x = np.linspace(0,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]

u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1)

r = float(sys.argv[1])
m = float(sys.argv[2])
plotname = str(sys.argv[3])



sigma = 0.45 
mu= 0
def gauss(x):
	return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(abs((L/float(2))-x)-mu)**2/(float(2*sigma**2)))


# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)

#for i in range(1,Nx):
#	A[i,i-1] = -C	
#	A[i,i+1] = -C	
#	A[i,i] = 1+2*C-D

A[0,0] = A[Nx,Nx] = 1

#Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
	u_1[i] = gauss(x[i])

err = 10**(-5)
for n in range(0, N):
	#Compute b and solve linear system
	#u[:] = r*u_1(1-u/float(m))
	out = True
	b[:] = u_1
	b[0]=b[Nx]=0
	while out == True:
		for i in range(1,Nx):
			A[i,i] = (1-dt*r*(1-u_[i]/m))
		A[0,0] = A[Nx,Nx] = 1
		u[:] = sl.solve(A, u_1)
		#u[:] = u_1/(1-dt*r*(1-u_/m))
		max_val = np.max(abs(u-u_))
		if(max_val <= err):
			out = False
		else:
			u_[:] = u
	np.save("%s%04d" % (plotname,n),u)
	#plt.plot(x,u)
	#plt.axis([0,2,-1,2])
	#plt.savefig("tmp%04d.png" % n)
	#plt.close()
	
	#Update u_1 and u_ before next step
	u_1[:] = u
	u_[:] = u




#os.system('avconv -r 10 -i %s -vcodec libvpx %s' %('tmp%04d.png',sys.argv[3]))

#for filename in glob.glob('tmp*.png'):
#	os.remove(filename)

#os.system('vlc testfile.webm')
#os.remove('testfile.mp4')
