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
		default=0.1, help='constant in the constant equation',
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
	parser.add_argument('--r', '--linear reproduction', type=float,
		default=0, help='linear reproduction',
		metavar='r')
	parser.add_argument('--M', '--carrying capasity', type=float,
		default=1, help='carrying capasity',
		metavar='M')
	parser.add_argument('--p_n', '--plot_name', type=str,
		default="img", help='plot_name',
		metavar='plot_name')
	parser.add_argument('--C1', '--Boundary left', type=float,
		default=0, help='Boundary left ',
		metavar='C1')
	parser.add_argument('--C2', '--Boundary right', type=float,
		default=0, help='Boundary right ',
		metavar='C2')
	parser.add_argument('--F', '--Flow in', type=float,
		default=0, help='Flow in',
		metavar='F')
	parser.add_argument('--err', '--err', type=float,
		default=1e-05, help='Tolerance in Picard',
		metavar='err')
	return parser

def read_command_line():
	parser = define_command_line_options()
	args = parser.parse_args()
	print
        'm={},k={},method={},movie_name={},picard={},r={},M={},plot_name={},C1={},C2={},F={},err={}'.format(args.m,args.k,args.method,args.m_n,args.picard,args.r,args.M, args.p_n,args.C1,args.C2,args.F,args.err)
	return args.m,args.k,args.method,args.m_n,args.picard,args.r,args.M,args.p_n,args.C1,args.C2,args.F,args.err

m,k,method,moviename,picard,r,M,plotname,C1,C2,F,err= read_command_line()

Nx = 20
N = 2000

L = 60
T = 10 

#List of values


x = np.linspace(-L,L,Nx+1)
dx = x[1]-x[0]
t = np.linspace(0,T,N+1)
dt = t[1]-t[0]
u = np.zeros(Nx+1)
u_1 = np.zeros(Nx+1)
u_ = np.zeros(Nx+1) #Picard

sigma = 0.45 
mu= 0
wavefront = True
if wavefront:
	q_w = 1
	s_w = 2/float(q_w)
	b_w = q_w/float(np.sqrt(2*(q_w+2)))
	c_w = (q_w+4)/float(np.sqrt(2*q_w+4))
	alpha_w = 1
	def initial_cond(x):
		return 1/((1+alpha_w*np.exp(b_w*(x)))**s_w)
else:
	def initial_cond(x):
		return (1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(abs((L/float(2))-x)-mu)**2/(float(2*sigma**2)))

# Data structures for the linear system
A = np.zeros([Nx+1,Nx+1])
b = np.zeros(Nx+1)
#time_d = sys.argv[2]

for i in range(0, Nx+1):
	u_1[i] = initial_cond(x[i])
u_[:] = u_1

#Choose the right equation
if(method == "constant"):
    def alpha(i):
        return k
elif(method == "abs_std"):
    def alpha(i):
        return (abs(u_[i+1]-u_[i])/float(dx))**m
elif(method == "ordinary"):
    def alpha(i):
        return 0.5*(u_[i]+u_[i+1])
else:
    sys.exit(1)

for i in range(1,Nx):
	A[i,i] = 1-dt*(r*(1-u_[i]/float(M))-(alpha(i)+alpha(i-1))/float(dx**2))
	A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
	A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))

A[0,0] = A[Nx,Nx] = 1
#Set initial condition u(x,0) = I(x)
np.save("%s0000" % plotname, u_1)
for n in range(0, N):
	out = True
	gamma = 0.2
	counter = 0
	out_now = 0
	b[:] = u_1
	if(F == 0 and wavefront):
		b[0] = 1
		b[Nx] = 0
	elif(F == 0):
		b[Nx]= b[0] = 0 
	else:
		b[0] += 2*C1*dx*(dt/float(dx**2))*(alpha(0))
		b[Nx] += 2*C2*dx*(dt/float(dx**2))*(alpha(Nx))
	if picard:
		while out == True:	#Doing 10 iterations before jumping to the next iteration
			for i in range(1,Nx):
				A[i,i] = 1-dt*(r*(1-u_[i]/float(M))-(alpha(i)+alpha(i-1))/float(dx**2))
				A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
				A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))
			A[0,0] = A[Nx,Nx] = 1+F*2*(dt/float(dx**2))*(alpha(i))
			A[0,1] = A[Nx,Nx-1] = -F*2*(dt/float(dx**2))*(alpha(i))
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
			A[i,i] = 1-dt*(r*(1-u_[i]/float(M))-(alpha(i)+alpha(i-1))/float(dx**2))
			A[i,i+1] = -(dt/float(dx**2))*(alpha(i))
			A[i,i-1] = -(dt/float(dx**2))*(alpha(i-1))
		A[0,0] = A[Nx,Nx] = 1+F*2*(dt/float(dx**2))*(alpha(i))
		A[0,1] = A[Nx,Nx-1] = -F*2*(dt/float(dx**2))*(alpha(i))
		u[:] = sl.solve(A, b)

	if(n%50 == 0):
		print "nr: ",n
		np.save("%s%04d" % (plotname,(n/50)+1),u)
	#Update u_1 and u_ before next step
	u_1[:] = u
	u_[:] = u



