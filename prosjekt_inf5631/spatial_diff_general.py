import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys


def define_command_line_options():
	import argparse
	parser = argparse.ArgumentParser()
	parser.add_argument('--m', '--power', type=float,
		default=1, help='power in the absolute equation',
		metavar='m')
	parser.add_argument('--k', '--constant', type=float,
		default=1, help='constant in the constant equation',
		metavar='k')
	parser.add_argument('--method', '--method', type=str,
		default="constant", help='function',
		metavar='method')
	parser.add_argument('--m_n', '--movie_name', type=str,
		default="testmovie.webm", help='movie_name',
		metavar='movie_name')
	parser.add_argument('--picard', '--picard', type= bool,
		default= False, help='turn on/off picard',
		metavar='picard')
	return parser

def read_command_line():
	parser = define_command_line_options()
	args = parser.parse_args()
	print
        'm={},k={},method={},movie_name={},picard={}'.format(args.m,args.k,args.method,args.m_n,args.picard)
	return args.m,args.k,args.method,args.m_n,args.picard

m,k,method,moviename,picard = read_command_line()



Nx = 200
N = 40

L = 10
T = 40 

#List of values
beta_0 = 1
beta_1 = 0.44
r = 1


x = np.linspace(0,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1) #Picard

sigma = 0.45 
mu= 0
def gauss(x):
	return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(abs((L/float(2))-x)-mu)**2/(float(2*sigma**2)))


# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)
#time_d = sys.argv[2]


for i in range(0, Nx+1):
	u_1[i] = gauss(x[i])
u_[:] = u_1

#Choose the right equation
if(method == "constant"):
    def alpha(i):
        return k
elif(method == "abs_std"):
    def alpha(i):
        return (abs(u_[i+1]-u_[i])/dx)**m
elif(method == "ordinary"):
    def alpha(i):
        return 0.5*(u_[i]+u_[i+1])
else:
    sys.exit(1)

for i in range(1,Nx):
	A[i,i] = 1+(dt/float(dx**2))*(alpha(i)+alpha(i-1))
	A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
	A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))
A[0,0] = A[Nx,Nx] = 1

err = 3*10**(-5)
#Set initial condition u(x,0) = I(x)

plt.plot(x,u_1)
plt.axis([0,L,-1,1])
plt.savefig("tmp%04d.png" % (0))
plt.close()
#plt.show()
for n in range(0, N):
	out = True
	gamma = 0.2
	counter = 0
	out_now = 0
	b[:] = u_1
	b[0] = b[Nx] = 0
        #print "kjor"
        if picard:
            while out == True:	#Doing 10 iterations before jumping to the next iteration
                for i in range(1,Nx):
                    A[i,i] = 1+(dt/float(dx**2))*(alpha(i)+alpha(i-1))
                    A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
                    A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))
                A[0,0] = A[Nx,Nx] = 1
                u[:] = sl.solve(A, b)
                max_val = np.max(abs(u-u_))
                #print "max: %f" % max_val
                if(max_val <= err):
                    out = False
                else:
                    u_[:]= gamma*u+(1-gamma)*u_ #Relaxation
                counter += 1
                if counter == 100:
                    gamma *= 0.99
                    print "count"
                    out_now += 1
                    if(out_now == 2):
                        out_now = 0
                        out = False
                    counter = 0
        else:
            for i in range(1,Nx):
                A[i,i] = 1+(dt/float(dx**2))*(alpha(i)+alpha(i-1))
                A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
                A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))
            A[0,0] = A[Nx,Nx] = 1
            u[:] = sl.solve(A, b)
        plt.plot(x,u)
	plt.axis([0,L,-1,1])
	if(n%1 == 0):
		print "nr: ",n
		plt.savefig("tmp%04d.png" % ((n/1)+1))
	plt.close()
	#Update u_1 and u_ before next step
	u_1[:] = u
	u_[:] = u


os.system('avconv -r 10 -i %s -vcodec libvpx %s' %('tmp%04d.png',moviename))

for filename in glob.glob('tmp*.png'):
	os.remove(filename)

