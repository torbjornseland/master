#Scrips for plotting figures and videos in Geographic models
import numpy as np
from plotmaker import *
import simple_PDE as si1D
import simple_PDE_2D as si2D
from english_school_2D import *
from LMR_zombie_model_PDE import *
from gamma_mapping import *

#SIR models

plotnames = ['images/Sub','images/Inf','images/Rem']
classnames = ['Susceptible', 'Infective','Removed']
parameter_values = ['Sub','Inf','Rem']
para_name = "Class"


#T = 34
#Nx = 10
#X = 10
#x0 = X/float(2)
#y0 = X/float(2)

#Find travelling wave point
"""
z_X = 15
z_Y = 15
z_xy = np.sqrt(z_X**2+z_Y**2) #Pythagoras
"""
def gauss_2D(x,y,a,sigma,x0,y0):
    return a*np.exp(-0.5*(((x-x0)**2/sigma)+((y-y0)**2/sigma)))

#Geographic models
#1D simple PDE
"""
T = 40
Nx = 100
Nt = 2000
X = 20
lam = 0.5
si1D.simple_PDE(T,Nx,Nt,X,lam)
"""

# A gaussian wave
"""
T = 40
X = 20
Nt = 100000
Nx = 50
lam = 0.5
z_X = 15
z_Y = 15
x0 = 0
y0 = 0
"""
"""
def init_func(x,y):
    return gauss_2D(x,y,0.2,0.5,x0,y)   

moviename = 'plots/2D_gaussian'
si2D.produce_plot(T,Nx,Nx,Nt,X,X,lam,z_X,z_Y,init_func,classnames,moviename,t_wave=True)
"""
# Gaussian corner
"""
moviename = 'plots/2D_gaussian_one_corner'
lam = 0.5
def init_func(x,y):
    return gauss_2D(x,y,0.2,0.5,x0,y0)   

si2D.produce_plot(T,Nx,Nx,Nt,X,X,lam,z_X,z_Y,init_func,classnames,moviename,t_wave=True)
"""
# Initial value
"""
moviename = 'plots/2D_initial_variable'
lam = 0.5
def init_func(x,y):
    return gauss_2D(x,y,1,5,x0,y0)

si2D.produce_plot(T,Nx,Nx,Nt,X,X,lam,z_X,z_Y,init_func,classnames,moviename,t_wave=True)
"""
#Tesing variation in lambda
"""
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


T = 15
Nt = 1000
X = 100
Nx = 100
z_X = z_Y = 0

rho = 202
r = 2.18*10**(-3)*(X**2)
a = r*rho/float(X**2)
D_s = D_i = D_r = 1

phases = [0,5,10,15]

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

english_school(T,Nx,Nx,Nt,X,X,z_X,z_Y,init_func,a,r,D_s,D_i,D_r,moviename,classnames,phases)
"""
# uniform spread with adjusted parameters

dx = X/float(Nx)
trav_name = "plots/boadring"
moviename = 'plots/2D_british_school'
volume_human = 0.0664
def init_func(x,y):
    return 1/float(X**2)
phases = [0,5,10,15]
max_val = (1/float(X**2))*762
english_school(T,Nx,Nx,Nt,X,X,z_X,z_Y,init_func,a,r,D_s,D_i,D_r,moviename,classnames,phases)
build_plot(plotnames,moviename,parameter_values,para_name,X,T,z_X,max_val)

# Gauss center
"""
moviename = 'plots/2D_british_school_gauss'
V = 1
A = 1
sig = np.sqrt(V/(2*np.pi*A))
x0 = X/float(2)
y0 = X/float(2)
def init_func(x,y):
    return gauss_2D(x,y,A,sig,x0,y0)

english_school(T,Nx,Nx,Nt,X,X,z_X,z_Y,init_func,a,r,D_s,D_i,D_r,moviename,classnames,phases)
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
# Zombiefication
"""
plotnames = ['images/Sub','images/Inf','images/Zom', 'images/Rem']
classnames = ['Susceptible', 'Infective', 'Zombies', 'Removed']
parameter_values = ['Sub','Inf','Zom','Rem']
para_name = "Class"
"""
# Initial phase
"""
T = 3
moviename = "plots/2D_zombie_initial_cond"
L = X
par_values = dict(Sigma=0,delta_S=0,delta_I=0,zeta=0,a=0.0073,sigma=0.005,mu=0.14)
def init_func(x,y):
    return 1
D_s = D_i = D_z = D_r = 1
"""
# Three phases

#Standard
"""
moviename = "plots/2D_zombie_three_phases"
D_s = D_i = D_z = D_r = 1
def init_func(x,y):
    return 1
"""
#Gauss from Center
"""
T = 34
D_s = D_i = D_z = 1
D_r = 0
Z_1 = np.zeros([Nx+3,Nx+3])  #list of Infective in previous time step
dx = X/float(Nx)
x,y = np.meshgrid(np.linspace(0-dx,X+dx,Nx+3),np.linspace(0-dx,X+dx,Nx+3))
V = 100
A = 50
sig = np.sqrt(V/float(2*np.pi*A))
def init_func(x,y):
    return gauss_2D(x,y,A,sig,x0,y0)


Z_1[:,:] = init_func(x,y)
"""
# Nt = 68000
"""
Nt = 68000
moviename = "plots/2D_zombie_three_phases_gauss"
"""
#Nt = 136000
"""
Nt = 136000
moviename = "plots/2D_zombie_three_phases_gauss_2"
"""
# Different initial and diffusion
"""
T = 34
Nt = 68000
Nx = 200
X = 20
#Z_1 = np.ones([Nx+3,Nx+3])*0.01
#S_1 = np.ones([Nx+3,Nx+3])
gamma_s = np.ones([Nx+3,Nx+3])
gamma_i = np.ones([Nx+3,Nx+3])#*0.5
gamma_z = np.ones([Nx+3,Nx+3])#*0.8

[gamma_s[1:-1,1:-1],gamma_i[1:-1,1:-1],gamma_z[1:-1,1:-1]] = gamma_mapping([gamma_s[1:-1,1:-1],gamma_i[1:-1,1:-1],gamma_z[1:-1,1:-1]])

#print gamma_s
#print gamma_i
#print gamma_z

#S_1[:,:Nx/2] = 0.5
z_X = z_Y = z_xy = 0
#moviename = "plots/2D_zombie_three_phases_initial_spread"
#moviename = "plots/2D_zombie_three_phases_initial_spread_2"
moviename = "plots/2D_zombie_three_phases_blindern_area_3_ph"
D_s = 1
D_i = 0.5
D_z = 0.9
D_r = 0
dx = X/float(Nx)
x,y = np.meshgrid(np.linspace(0-dx,X+dx,Nx+3),np.linspace(0-dx,X+dx,Nx+3))
"""
#Initial conditions for Zombies
"""
V = 1
A = 0.2
sig = V/float(2*np.pi*A)
Z_1 = gauss_2D(x,y,A,sig,10,10)
"""
#Initial conditions for Susceptible
"""
V_s = 21
A_s = 0.5
sig_s = V_s/float(2*np.pi*A_s)
S_1 = gauss_2D(x,y,A_s,sig_s,4,4)

V_s = 200
A_s = 3
sig_s = V_s/float(2*np.pi*A_s)
S_1 += gauss_2D(x,y,A_s,sig_s,9,15)

V_s = 400
A_s = 4
sig_s = V_s/float(2*np.pi*A_s)
S_1 += gauss_2D(x,y,A_s,sig_s,15,5)

#S_1 = init_func(x,y,5,8)*200
#S_1 += init_func(x,y,3,3)*400
#S_1 *= 621/float(Nx**2)

if S_1.max() >= Z_1.max():
    max_val = S_1.max()
else:
    max_val = Z_1.max()
"""
#parameter values
"""
av = (Nx**2)
par_values = dict(Sigma=3.45*10**(-5),delta_S=2.2*10**(-5),delta_I=2.2*10**(-5),zeta=0,a=0.0073*X**2,sigma=0.005,mu=0.14)
attacks = [33.125]
phases = [0,3]#,33,34]
def beta(t):
    if t < 3:
        return 0.01155*X**2
    else:
        return 0.000011*X**2
def rho(t):
    if t < 3:
        return 1.37
    else:
        return 1.5
def alpha(t):
    if t < 3:
        return 0.00044*X**2
    else:
        return 0.000208*X**2

"""

#zombiefication_2D(T,Nx,Nx,Nt,X,X,z_X,z_Y,D_s,D_i,D_z,D_r,moviename,par_values,classnames,beta,rho,alpha,attacks,phases,Z_1,S_1,gamma_s,gamma_i,gamma_z)

#build_plot(plotnames,moviename,parameter_values,para_name,X,T,z_xy,max_val)
#sub_plot(plotnames,moviename,parameter_values,para_name,X,T,z_xy,max_val,classnames)
#contourf_plot(plotnames,moviename,parameter_values,para_name,X,T,z_xy,max_val,classnames)
os.system('rm images/*')
#plt.plot(r,I_1)
#plt.plot(r,S_1)
#plt.show()
