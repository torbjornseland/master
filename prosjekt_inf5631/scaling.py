import numpy as np
import scipy.linalg as sl
import matplotlib.pyplot as plt
import os,glob,sys


sigma = 0.45 
mu= 0
def initial_cond(x,t,m,L):
	return ((1/(sigma*np.sqrt(2*np.pi)))*np.exp(-(abs((L/float(2))-x)-mu)**2/(float(2*sigma**2)))/float(m))

def scaling(plotname,Nx,N,L,T,m):
	#plotname = "plot_data/test"

	#List of values
	x = np.linspace(0,L,Nx+1)
	dx = x[1]-x[0]
	t = np.linspace(0,T,N+1)
	dt = t[1]-t[0]
	u = np.zeros(Nx+1)
	u_1 = np.zeros(Nx+1)
	
	for i in range(0, Nx+1):
		u_1[i] = initial_cond(x[i],0,m,L)
	

	for n in range(0, N+1):
		u[:] = u_1*(1+dt*(1-u_1)) 
		np.save("%s%04d" % (plotname,n),u)
		u_1[:] = u

