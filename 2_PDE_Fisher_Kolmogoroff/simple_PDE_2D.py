import numpy as np
from plotmaker import *

def produce_plot(T,Nx,Ny,Nt,X,Y,lam,z_X,z_Y,init_func,classnames,t_wave=False):
    
    S = np.zeros([Nx+3,Ny+3])   #list of Susceptible
    S_1 = np.ones([Nx+3,Ny+3])  #list of Susceptible in previous time step
    I = np.zeros([Nx+3,Ny+3])   #list of Infective
    I_1 = np.zeros([Nx+3,Ny+3]) #list of Infective in previous time step
    R = np.zeros([Nx+3,Ny+3])   #list of Removed 
    R_1 = np.zeros([Nx+3,Ny+3]) #list of Removed in previous time step

    S_vol = np.zeros([Nt+1])
    I_vol = np.zeros([Nt+1])
    R_vol = np.zeros([Nt+1])

    dx = X/float(Nx)
    dy = X/float(Ny)

    x,y = np.meshgrid(np.linspace(0-dx,X+dx,Nx+3),np.linspace(0-dy,Y+dy,Ny+3))
    #x = np.linspace(0-dx,X+dx,Nx+3)
    #y = np.linspace(0-dy,X+dy,Ny+3)
    t = np.linspace(0,T,Nt+1)

    dt = t[1]-t[0]

    #Check travelling wave
    if trav_wave:
        z = np.zeros(Nt+1)
        z_S = np.zeros(Nt+1)
        z_I = np.zeros(Nt+1)
        z_R = np.zeros(Nt+1)
        z_x = int(z_X/dx)
        z_y = int(z_Y/dy)
        z_xy = np.sqrt(z_X**2+z_Y**2) #Pythagoras

    I_1[:,:] = init_func(x,y) #starts with a init func 
    #I_1[:] += 0.1

    #Volume
    S_vol[0] = volume_engine(S_1[1:-1,1:-1],dx*dy)
    I_vol[0] = volume_engine(I_1[1:-1,1:-1],dx*dy)
    R_vol[0] = volume_engine(R_1[1:-1,1:-1],dx*dy)
    
    np.save("images/Sub%04d" % 0,S_1[1:-1,1:-1]) #initial conditions
    np.save("images/Inf%04d" % 0,I_1[1:-1,1:-1]) #initial conditions
    np.save("images/Rem%04d" % 0,R_1[1:-1,1:-1]) #initial conditions

    #Initial cond for travelling wave
    if trav_wave:
        z[0] = z_xy
        z_S[0] = S_1[z_x,z_y]
        z_I[0] = I_1[z_x,z_y]
        z_R[0] = R_1[z_x,z_y]

    for n in range(1,Nt+1):
        S[1:-1,1:-1] = S_1[1:-1,1:-1] + dt*(-S_1[1:-1,1:-1]*I_1[1:-1,1:-1]+(((S_1[:-2,1:-1]-2*S_1[1:-1,1:-1]+S_1[2:,1:-1])/dx**2)+((S_1[1:-1,:-2]-2*S_1[1:-1,1:-1]+S_1[1:-1,2:])/dy**2)))
        I[1:-1,1:-1] = I_1[1:-1,1:-1] + dt*(S_1[1:-1,1:-1]*I_1[1:-1,1:-1]-lam*I_1[1:-1,1:-1]+(((I_1[:-2,1:-1]-2*I_1[1:-1,1:-1]+I_1[2:,1:-1])/dx**2)+((I_1[1:-1,:-2]-2*I_1[1:-1,1:-1]+I_1[1:-1,2:])/dy**2)))
        R[1:-1,1:-1] = R_1[1:-1,1:-1] + dt*(lam*I_1[1:-1,1:-1]+(((R_1[:-2,1:-1]-2*R_1[1:-1,1:-1]+R_1[2:,1:-1])/dx**2)+((R_1[1:-1,:-2]-2*R_1[1:-1,1:-1]+R_1[1:-1,2:])/dy**2)))

        if trav_wave:
            z[n] = z_xy-n*dt
            z_S[n] = S[z_x,z_y]
            z_I[n] = I[z_x,z_y]
            z_R[n] = R[z_x,z_y]

        S[0,:] = S[2,:]
        S[-1,:] = S[-3,:]
        S[:,0] = S[:,2]
        S[:,-1] = S[:,-3]
        
        I[0,:] = I[2,:]
        I[-1,:] = I[-3,:]
        I[:,0] = I[:,2]
        I[:,-1] = I[:,-3]
        
        R[0,:] = R[2,:]
        R[-1,:] = R[-3,:]
        R[:,0] = R[:,2]
        R[:,-1] = R[:,-3]
        
        #Volume
        S_vol[n] = volume_engine(S[1:-1,1:-1],dx*dy)
        I_vol[n] = volume_engine(I[1:-1,1:-1],dx*dy)
        R_vol[n] = volume_engine(R[1:-1,1:-1],dx*dy)

        if (n%40 == 0):
            np.save("images/Sub%04d" % (n/40),S[1:-1,1:-1])
            np.save("images/Inf%04d" % (n/40),I[1:-1,1:-1])
            np.save("images/Rem%04d" % (n/40),R[1:-1,1:-1])

        S_1[:,:] = S
        I_1[:,:] = I 
        R_1[:,:] = R 

    z_list = [z_S,z_I,z_R] 
    trav_wave(Nt,z,z_list,classnames,z_X,'2D')
    #plot_volume(t,S_vol,I_vol,R_vol)


