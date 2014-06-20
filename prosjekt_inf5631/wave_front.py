import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys

def wave_front(plotname,Nx,N,L,T):
	#plotname = "plot_data/test"

	#List of values
	x = np.linspace(-L,L,Nx+1)
	dx = x[1]-x[0]
	t = np.linspace(0,T,N+1)
	dt = t[1]-t[0]
	u = np.zeros(Nx+1)
	u_1 = np.zeros(Nx+1)
	u_ = np.zeros(Nx+1) #Picard

	q = 1
	s = 2/float(q)
	b = q/float(np.sqrt(2*(q+2)))
	c = (q+4)/float(np.sqrt(2*q+4))
	print "c",c
	alpha = 1
	def reverse_exact_u(x,t):
		return 1/((1+alpha*np.exp(b*(x-c*t)))**s)


	for n in range(0, N+1):
		u[:] = reverse_exact_u(x,t[n])
		np.save("%s%04d" % (plotname,n),u)

