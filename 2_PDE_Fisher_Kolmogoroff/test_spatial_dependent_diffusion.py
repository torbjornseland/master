import numpy as np
from plotmaker import *

def omega(t, a, sigma, T):
    return a*sum(np.exp(-0.5*(t-T[i])**2/sigma) for i in range(len(T)))

def zombiefication_2D(T,Nx,Ny,Nt,X,Y,z_X,z_Y,moviename,par_values,classnames,beta,rho,alpha,attacks,phases,Z_1,S_1,gamma_s,gamma_i,gamma_z,title,folder,gap):
    #parameters
    """
    Sigma = par_val[0]
    beta = par_val[1]
    delta_S = par_val[2]
    delta_I = par_val[3]
    rho = par_val[4]
    zeta = par_val[5]
    alpha = par_val[6]
    a = par_val[7]
    sigma = par_val[8]
    """
    mn = int(Nt/100) #movie number, choose 100 uniformly distributed
    print mn
    for args in par_values:
        exec("%s = %f" % (args, par_values[args]))

    S = np.zeros([Nx+3,Ny+3])   #list of Susceptible
    #S_1 = np.ones([Nx+3,Ny+3])  #list of Susceptible in previous time step
    
    I = np.zeros([Nx+3,Ny+3])   #list of Infective
    I_1 = np.zeros([Nx+3,Ny+3])  #list of Infective in previous time step

    Z = np.zeros([Nx+3,Ny+3])   #list of Infective
    #Z_1 = np.zeros([Nx+3,Ny+3]) #list of Infective in previous time step
    
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

    #Z_1[:,:] = init_func(x,y,5,8) #starts with a init func 
    #S_1[:,:] *= 621 
    #S_1[:,:] = init_func(x,y,5,8)*200 #starts with a init func 
    #S_1[:,:] += init_func(x,y,3,3)*400 #starts with a init func 
    #S_1[:,:] += init_func(x,y,8)*21 #starts with a init func 
    #I_1[:] += 0.1
    
    #Volume
    S_vol[0] = volume_engine(S_1[1:-1,1:-1],dx*dy)
    print "initial vol S",S_vol[0]
    I_vol[0] = volume_engine(I_1[1:-1,1:-1],dx*dy)
    Z_vol[0] = volume_engine(Z_1[1:-1,1:-1],dx*dy)
    R_vol[0] = volume_engine(R_1[1:-1,1:-1],dx*dy)

    np.savez_compressed("%s/Sub%04d" % (folder,0),S_1[1:-1:gap,1:-1:gap]) #initial conditions
    np.savez_compressed("%s/Inf%04d" % (folder,0),I_1[1:-1:gap,1:-1:gap]) #initial conditions
    np.savez_compressed("%s/Zom%04d" % (folder,0),Z_1[1:-1:gap,1:-1:gap]) #initial conditions
    np.savez_compressed("%s/Rem%04d" % (folder,0),R_1[1:-1:gap,1:-1:gap]) #initial conditions

        
    
        #Initial cond for travelling wave
    if (T != 0):
        for n in range(1,Nt+1): 
            if (n*dt % 1 == 0):
                print n*dt
            omega_t = omega(t[n], a, sigma, attacks)

            # Only diffusion as a constant
            """
            S[1:-1,1:-1] = S_1[1:-1,1:-1] + dt*(Sigma -(beta(t[n])+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-delta_S*S_1[1:-1,1:-1]+\
                    D_s*(((S_1[:-2,1:-1]-2*S_1[1:-1,1:-1]+S_1[2:,1:-1])/dx**2)+((S_1[1:-1,:-2]-2*S_1[1:-1,1:-1]+S_1[1:-1,2:])/dy**2)))
            I[1:-1,1:-1] = I_1[1:-1,1:-1] + dt*((beta(t[n])+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-rho(t[n])*I_1[1:-1,1:-1]-delta_I*I_1[1:-1,1:-1]+\
                    D_i*(((I_1[:-2,1:-1]-2*I_1[1:-1,1:-1]+I_1[2:,1:-1])/dx**2)+((I_1[1:-1,:-2]-2*I_1[1:-1,1:-1]+I_1[1:-1,2:])/dy**2)))
            Z[1:-1,1:-1] = Z_1[1:-1,1:-1] + dt*(rho(t[n])*I_1[1:-1,1:-1]-(alpha(t[n]) + omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]+zeta*R_1[1:-1,1:-1]+\
                    D_z*(((Z_1[:-2,1:-1]-2*Z_1[1:-1,1:-1]+Z_1[2:,1:-1])/dx**2)+((Z_1[1:-1,:-2]-2*Z_1[1:-1,1:-1]+Z_1[1:-1,2:])/dy**2)))
            R[1:-1,1:-1] = R_1[1:-1,1:-1] + dt*(delta_S*S_1[1:-1,1:-1]+delta_I*I_1[1:-1,1:-1]-zeta*R_1[1:-1,1:-1]+(alpha(t[n]) + omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]+\
                    D_r*(((R_1[:-2,1:-1]-2*R_1[1:-1,1:-1]+R_1[2:,1:-1])/dx**2)+((R_1[1:-1,:-2]-2*R_1[1:-1,1:-1]+R_1[1:-1,2:])/dy**2)))
            """
            # Controlled by gamma(x)
            S[1:-1,1:-1] = S_1[1:-1,1:-1] + dt*(Sigma -(beta(t[n])+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-delta_S*S_1[1:-1,1:-1]+\
                    ((gamma_s[:-2,1:-1]+gamma_s[1:-1,1:-1])*(S_1[:-2,1:-1]-S_1[1:-1,1:-1]))/(2*dx**2)-\
                    ((gamma_s[2:,1:-1]+gamma_s[1:-1,1:-1])*(S_1[1:-1,1:-1]-S_1[2:,1:-1]))/(2*dx**2)+\
                    ((gamma_s[1:-1,:-2]+gamma_s[1:-1,1:-1])*(S_1[1:-1,:-2]-S_1[1:-1,1:-1]))/(2*dy**2)-\
                    ((gamma_s[1:-1,2:]+gamma_s[1:-1,1:-1])*(S_1[1:-1,1:-1]-S_1[1:-1,2:]))/(2*dy**2))
            I[1:-1,1:-1] = I_1[1:-1,1:-1] + dt*((beta(t[n])+mu*omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]-rho(t[n])*I_1[1:-1,1:-1]-delta_I*I_1[1:-1,1:-1]+
                    ((gamma_i[:-2,1:-1]+gamma_i[1:-1,1:-1])*(I_1[:-2,1:-1]-I_1[1:-1,1:-1]))/(2*dx**2)-\
                    ((gamma_i[2:,1:-1]+gamma_i[1:-1,1:-1])*(I_1[1:-1,1:-1]-I_1[2:,1:-1]))/(2*dx**2)+\
                    ((gamma_i[1:-1,:-2]+gamma_i[1:-1,1:-1])*(I_1[1:-1,:-2]-I_1[1:-1,1:-1]))/(2*dy**2)-\
                    ((gamma_i[1:-1,2:]+gamma_i[1:-1,1:-1])*(I_1[1:-1,1:-1]-I_1[1:-1,2:]))/(2*dy**2))
            Z[1:-1,1:-1] = Z_1[1:-1,1:-1] + dt*(rho(t[n])*I_1[1:-1,1:-1]-(alpha(t[n]) + omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1]+zeta*R_1[1:-1,1:-1]+
                    ((gamma_z[:-2,1:-1]+gamma_z[1:-1,1:-1])*(Z_1[:-2,1:-1]-Z_1[1:-1,1:-1]))/(2*dx**2)-\
                    ((gamma_z[2:,1:-1]+gamma_z[1:-1,1:-1])*(Z_1[1:-1,1:-1]-Z_1[2:,1:-1]))/(2*dx**2)+\
                    ((gamma_z[1:-1,:-2]+gamma_z[1:-1,1:-1])*(Z_1[1:-1,:-2]-Z_1[1:-1,1:-1]))/(2*dy**2)-\
                    ((gamma_z[1:-1,2:]+gamma_z[1:-1,1:-1])*(Z_1[1:-1,1:-1]-Z_1[1:-1,2:]))/(2*dy**2))
            R[1:-1,1:-1] = R_1[1:-1,1:-1] + dt*(delta_S*S_1[1:-1,1:-1]+delta_I*I_1[1:-1,1:-1]-zeta*R_1[1:-1,1:-1]+(alpha(t[n]) + omega_t)*S_1[1:-1,1:-1]*Z_1[1:-1,1:-1])

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
            I_vol[n] = volume_engine(I[1:-1,1:-1],dx*dy)
            Z_vol[n] = volume_engine(Z[1:-1,1:-1],dx*dy)
            R_vol[n] = volume_engine(R[1:-1,1:-1],dx*dy)

            if (n%mn == 0):
                np.savez_compressed("%s/Sub%04d" % (folder,(n/mn)),S[1:-1:gap,1:-1:gap])
                np.savez_compressed("%s/Inf%04d" % (folder,(n/mn)),I[1:-1:gap,1:-1:gap])
                np.savez_compressed("%s/Zom%04d" % (folder,(n/mn)),Z[1:-1:gap,1:-1:gap])
                np.savez_compressed("%s/Rem%04d" % (folder,(n/mn)),R[1:-1:gap,1:-1:gap])
			print "S",S[2]	
            S_1[:,:] = S
            I_1[:,:] = I
            Z_1[:,:] = Z 
            R_1[:,:] = R 

    plot_volume(t,[S_vol,I_vol,Z_vol,R_vol],moviename,classnames,T,title)
    print_phase(dt,t,phases,[S_vol,I_vol,Z_vol,R_vol],classnames)


