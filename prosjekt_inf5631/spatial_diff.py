import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys

Nx = 20000
N = 200

L = 10
T = 1

beta_0 = 1
beta_1 = 0.44
r = 1
m = 10
k = float(sys.argv[1])


x = np.linspace(0,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1) #Picard


def I(x):
	return (1-(x-1)**2)

sigma = 0.45 
mu= 0
def gauss(x):
	return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(abs((L/float(2))-x)-mu)**2/(float(2*sigma**2)))


# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)
time_d = sys.argv[2]
if(time_d == "constant"):
	def K_1(x):
		return dt*k/float(dx**2) 
	def K_2(x):
		return dt*k/float(dx**2) 
elif(time_d == "abs_std"):
	m = float(sys.argv[4])
	def K_1(i):
		return dt*(abs(u_[i]-u_[i-1])**m/dx**3) 
	def K_2(i):
		return dt*(abs(u_[i+1]-u_[i])**m/dx**3) 
elif(time_d == "ordinary"):
	def K_1(i):
		return dt*(u_[i]-u_[i-1])/(2*dx**2) 
	def K_2(i):
		return dt*(u_[i+1]-u_[i])/(2*dx**2) 
else:
	sys.exit(0)

for i in range(1,Nx):
	A[i,i-1] = -K_1(i)
	A[i,i+1] = -K_2(i)
	A[i,i] = 1+K_1(i)+K_2(i)
A[0,0] = A[Nx,Nx] = 1

err = 3*10**(-5)
#Set initial condition u(x,0) = I(x)
for i in range(0, Nx+1):
	u_1[i] = gauss(x[i])


#plt.plot(x,u_1)
#plt.axis([0,10,-1,1])
#plt.show()

for n in range(0, N):
	#Updates the whole matrix
	out = True
	alpha = 0.2
	counter = 0
	out_now = 0
	
	b[:] = u_1
	b[0] = b[Nx] = 0
	if(time_d != "constant"):
		while out == True:	#Doing 10 iterations before jumping to the next iteration
			for i in range(1,Nx):
				A[i,i-1] = -K_1(i)
				A[i,i+1] = -K_2(i)
				A[i,i] = 1+K_1(i)+K_2(i)
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
	plt.axis([0,L,-1,1])
	if(n%10 == 0):
		print "nr: ",n
		plt.savefig("tmp%04d.png" % (n/10))
	plt.close()
	#Update u_1 and u_ before next step
	u_1[:] = u
	u_[:] = u



os.system('avconv -r 10 -i %s -vcodec libvpx %s' %('tmp%04d.png',sys.argv[3]))

for filename in glob.glob('tmp*.png'):
	os.remove(filename)

