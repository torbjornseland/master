import numpy as np
from plotmaker import *

def zombiefication_2D(T,Nx,Ny,Nt,X,Y,z_X,z_Y,init_func,D_s,D_i,D_r,moviename,par_values):
    #parameters
    Sigma = par_val[0]
    beta = par_val[1]
    delta_S = par_val[2]
    delta_I = par_val[3]
    rho = par_val[4]
    zeta = par_val[5]
    alpha = par_val[6]
    a = par_val[7]
    sigma = par_val[8]


    S = np.zeros([Nx+3,Ny+3])   #list of Susceptible
    S_1 = np.ones([Nx+3,Ny+3])  #list of Susceptible in previous time step
    
    I = np.zeros([Nx+3,Ny+3])   #list of Infective
    I_1 = np.zeros([Nx+3,Ny+3])  #list of Infective in previous time step

    Z = np.zeros([Nx+3,Ny+3])   #list of Infective
    Z_1 = np.zeros([Nx+3,Ny+3]) #list of Infective in previous time step
    
    R = np.zeros([Nx+3,Ny+3])   #list of Removed 
    R_1 = np.zeros([Nx+3,Ny+3]) #list of Removed in previous time step

    S_vol = np.zeros([Nt+1])
    I_vol = np.zeros([Nt+1])
    Z_vol = np.zeros([Nt+1])
    R_vol = np.zeros([Nt+1])

    dx = X/float(Nx)
    dy = X/float(Ny)

    x,y = np.meshgrid(np.linspace(0-dx,X+dx,Nx+3),np.linspace(0-dy,Y+dy,Ny+3))
    #x = np.linspace(0-dx,X+dx,Nx+3)
    #y = np.linspace(0-dy,X+dy,Ny+3)
    t = np.linspace(0,T,Nt+1)

    dt = t[1]-t[0]


    Z_1[:,:] = init_func(x,y) #starts with a init func 
    #S_1[:,:] *= 762 #starts with a init func 
    #I_1[:] += 0.1
    
    #Volume
    S_vol[0] = volume_engine(S_1[1:-1,1:-1],dx*dy)
    I_vol[0] = volume_engine(S_1[1:-1,1:-1],dx*dy)
    Z_vol[0] = volume_engine(Z_1[1:-1,1:-1],dx*dy)
    R_vol[0] = volume_engine(R_1[1:-1,1:-1],dx*dy)

    np.save("images/Sub%04d" % 0,S_1[1:-1,1:-1]) #initial conditions
    np.save("images/Inf%04d" % 0,Z_1[1:-1,1:-1]) #initial conditions
    np.save("images/Zom%04d" % 0,Z_1[1:-1,1:-1]) #initial conditions
    np.save("images/Rem%04d" % 0,R_1[1:-1,1:-1]) #initial conditions

    #Initial cond for travelling wave
    for n in range(1,Nt+1):
        S[1:-1,1:-1] = S_1[1:-1,1:-1] + dt*(Sigma -(beta+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-delta_S*S_1[1:-1,1:-1]+D_s*(((S_1[:-2,1:-1]-2*S_1[1:-1,1:-1]+S_1[2:,1:-1])/dx**2)+((S_1[1:-1,:-2]-2*S_1[1:-1,1:-1]+S_1[1:-1,2:])/dy**2)))
        I[1:-1,1:-1] = I_1[1:-1,1:-1] + dt*((beta+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-rho*I_1[1:-1,1:-1]-delta_I*I_1[1:-1,1:-1] +D_i*(((I_1[:-2,1:-1]-2*I_1[1:-1,1:-1]+I_1[2:,1:-1])/dx**2)+((I_1[1:-1,:-2]-2*I_1[1:-1,1:-1]+I_1[1:-1,2:])/dy**2)))
        Z[1:-1,1:-1] = Z_1[1:-1,1:-1] + dt*(rho*I_1[1:-1,1:-1]-(alpha + omega_t)*S_[1:-1,1:-1]*Z_1[1:-1,1:-1]+zeta*R[1:-1,1:-1]+D_z*(((Z_1[:-2,1:-1]-2*Z_1[1:-1,1:-1]+Z_1[2:,1:-1])/dx**2)+((Z_1[1:-1,:-2]-2*Z_1[1:-1,1:-1]+Z_1[1:-1,2:])/dy**2)))
        R[1:-1,1:-1] = R_1[1:-1,1:-1] + dt*(delta_S*S_1[1:-1,1:-1]+delta_I*I_1[1:-1,1:-1]-zeta*R[1:-1,1:-1]+(alpha + omega_t)*S_[1:-1,1:-1]*Z_1[1:-1,1:-1]+D_r*(((R_1[:-2,1:-1]-2*R_1[1:-1,1:-1]+R_1[2:,1:-1])/dx**2)+((R_1[1:-1,:-2]-2*R_1[1:-1,1:-1]+R_1[1:-1,2:])/dy**2)))

        S[0,:] = S[2,:]
        S[-1,:] = S[-3,:]
        S[:,0] = S[:,2]
        S[:,-1] = S[:,-3]

        I[0,:] = I[2,:]
        I[-1,:] = I[-3,:]
        I[:,0] = I[:,2]
        I[:,-1] = I[:,-3]
        
        Z[0,:] = Z[2,:]
        Z[-1,:] = Z[-3,:]
        Z[:,0] = Z[:,2]
        Z[:,-1] = Z[:,-3]
        
        R[0,:] = R[2,:]
        R[-1,:] = R[-3,:]
        R[:,0] = R[:,2]
        R[:,-1] = R[:,-3]

        #Volume
        S_vol[n] = volume_engine(S[1:-1,1:-1],dx*dy)
        Z_vol[n] = volume_engine(Z[1:-1,1:-1],dx*dy)
        R_vol[n] = volume_engine(R[1:-1,1:-1],dx*dy)

        if (n%40 == 0):
            np.save("images/Sub%04d" % (n/40),S[1:-1,1:-1])
            np.save("images/Inf%04d" % (n/40),Z[1:-1,1:-1])
            np.save("images/Rem%04d" % (n/40),R[1:-1,1:-1])

        S_1[:,:] = S
        Z_1[:,:] = Z 
        R_1[:,:] = R 

    plot_volume(t,S_vol,Z_vol,R_vol,moviename)
