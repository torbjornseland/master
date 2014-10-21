#Scrips for plotting figures and videos in Geographic models
import numpy as np
from plotmaker import *
from simple_PDE_2D import *
from english_school_2D import *


T = 15
Nx = 100
Nt = 8000
X = 10
x0 = X/float(2)
y0 = X/float(2)

#Find travelling wave point
z_X = 15
z_Y = 15
z_xy = np.sqrt(z_X**2+z_Y**2) #Pythagoras
def gauss_2D(x,y,a,sigma,x0,y0):
    return a*np.exp(-0.5*(((x-x0)**2/sigma)+((y-y0)**2/sigma)))


"""
moviename = 'plots/2D_gaussian'
lam = 0.5
"""
"""
moviename = 'plots/2D_one_corner'
lam = 0.5
def init_func(x,y):
    return gauss_2D(x,y,0.2,0.5,x0,y0)   
"""
"""
moviename = 'plots/2D_initial_variable'
lam = 0.5
def init_func(x,y):
    return gauss_2D(x,y,1,5,x0,y0)
"""
"""
#Tesing variation in lambda
def init_func(x,y):
    return gauss_2D(x,y,0.2,0.5,x0,y0)   
lam_list = [0.01,0.3,0.7,1]
n = 1
for lam in lam_list:
    trav_name = "plots/lambda_%i" % n
    produce_plot(T,Nx,Nx,Nt,X,X,lam,z_X,z_Y,init_func,trav_name,trav_wave=True)
    n += 1
os.system('doconce combine_images plots/lambda_* plots/2D_lambda_variable.png')
os.system('rm plots/lambda_*')
"""

#English boarding school
#uniform spread
"""
trav_name = "plots/boadring"
moviename = 'plots/2D_british_school'
rho = 202
r = 2.18*10**(-3)
a = r*rho
#a = 202/float(762)
D_s = D_i = D_r = 1
A = 0.5
sig = 13/(2*np.pi)
#def init_func(x,y):
#    return gauss_2D(x,y,A,sig,x0,y0)
def init_func(x,y):
    return 1
"""
# Gauss center
"""
moviename = 'plots/2D_british_school_gauss'
rho = 202
r = 2.18*10**(-3)
a = r*rho
D_s = D_i = D_r = 1
V = 100
A = 50
sig = np.sqrt(V/(2*np.pi*A))

def init_func(x,y):
    return gauss_2D(x,y,A,sig,x0,y0)
"""
#Gauss corner
"""
moviename = 'plots/2D_british_school_gauss_corner'
rho = 202
r = 2.18*10**(-3)
a = r*rho
D_s = D_i = D_r = 1
x0=0
y0=0
V = 400
A = 100
sig = np.sqrt(V/(2*np.pi*A))

def init_func(x,y):
    return gauss_2D(x,y,A,sig,x0,y0)
"""

plotnames = ['images/Sub','images/Inf','images/Zom', 'images/Rem']
parameter_values = ['Sub','Inf','Zom','Rem']
para_name = "Class"
L = X


#english_school(T,Nx,Nx,Nt,X,X,z_X,z_Y,init_func,a,r,D_s,D_i,D_r,moviename)
zombiefication(T,Nx,Nx,Nt,X,X,z_X,z_Y,init_func,a,r,D_s,D_i,D_r,moviename)

build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_xy)
os.system('rm images/*')
#plt.plot(r,I_1)
#plt.plot(r,S_1)
#plt.show()
