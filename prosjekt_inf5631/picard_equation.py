import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob

Nx = 100
N = 200

L = 2
T = 2

beta_0 = 1
beta_1 = 0.44
r = 1
m = 10



x = np.linspace(0,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1) #Picard

def C(u_):
	return ((beta_0+beta_1*u_)*dt)/(2*dx**2)

def D(u_):
	return dt*r*(1-(u_/float(m)))*0.5

def I(x):
	return (1-(x-1)**2)


# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)

A[0,0] = A[Nx,Nx] = 1

err = 3*10**(-5)
#Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
	u_1[i] = I(x[i])


for n in range(0, N):
	#Updates the whole matrix
	out = True
	alpha = 0.2
	counter = 0
	out_now = 0
	while out == True:	#Doing 10 iterations before jumping to the next iteration
		for i in range(1,Nx):
			A[i,i-1] = -C((u_[i+1]-u_[i])/dx)
			A[i,i+1] = -C((u_[i+1]-u_[i])/dx)
			A[i,i] = 1+2*C((u_[i+1]-u_[i])/dx)-D(u_[i])
		for i in range(1, Nx):
			b[i] = (1-2*C((u_[i+1]-u_[i])/dx)+D(u_[i]))*u_1[i]+C((u_[i+1]-u_[i])/dx)*(u_1[i-1]+u_1[i+1])
		b[0] = b[Nx] = 0
		u[:] = sl.solve(A, b)
		max_val = np.max(abs(u-u_))
		#print "max: %f" % max_val
		if(max_val <= err):
			#print "out"
			out = False
		else:
			u_[:]= alpha*u+(1-alpha)*u_ #Relaxation
		counter += 1
		if counter == 100:
			alpha *= 0.99
			print "count"
			out_now += 1
			if(out_now == 2):
				out_now = 0
				out = False
			counter = 0
	plt.plot(x,u)
	plt.axis([0,2,-1,1])
	if(n%10 == 0):
		print "nr: ",n
		plt.savefig("tmp%04d.png" % (n/10))
	plt.close()
	#Update u_1 and u_ before next step
	u_1[:] = u
	u_[:] = u



os.system('avconv -r 10 -i %s -vcodec mpeg4 %s' %('tmp%04d.png','testfile.mp4'))

for filename in glob.glob('tmp*.png'):
	os.remove(filename)

os.system('vlc testfile.mp4')
os.remove('testfile.mp4')
