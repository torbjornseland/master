import glob,os
import numpy as np
import matplotlib.pyplot as plt
from plotmaker import trav_wave


def simple_PDE(T,Nx,Nt,X,lam,beta,S_1,I_1,R_1,f,g,h):
    S = np.zeros(Nx+3)   #list of Susceptible
    #S_1 = np.ones(Nx+1)#list of Susceptible in previous time step
    I = np.zeros(Nx+3)   #list of Susceptible
    #I_1 = np.zeros(Nx+1)#list of Susceptible in previous time step
    R = np.zeros(Nx+3)   #list of Susceptible
    #R_1 = np.zeros(Nx+1)#list of Susceptible in previous time step
    print T
    print Nt

    x = np.linspace(0,X,Nx+1)
    t = np.linspace(0,T,Nt+1)

    dt = t[1]-t[0]
    dx = x[1]-x[0]
    print "dt=",dt
    print "dx=",dx
    print "dx^2=",dx**2

    #Check travelling wave
    z = np.zeros(Nt+1)
    z_S = np.zeros(Nt+1)
    z_I = np.zeros(Nt+1)
    z_R = np.zeros(Nt+1)
    z_X = 15
    z_i = int(z_X/dx)

    def gauss(t,a,sigma,T):
        return a*np.exp(-0.5*(t-T)**2/sigma)

    #I_1[:] = gauss(x,0.2,0.5,0) #starts with a gauss function
    #I_1[:] += 0.1

    np.save("images/Sub%04d" % 0,S_1) #initial conditions
    np.save("images/Inf%04d" % 0,I_1) #initial conditions
    np.save("images/Rem%04d" % 0,R_1) #initial conditions

    #Initial cond for travelling wave
    """
    z[0] = z_X
    z_S[0] = S_1[z_i]
    z_I[0] = I_1[z_i]
    z_R[0] = R_1[z_i]
    """
    #print "S---------------------"
    #print S_1[1:-1]

    #def lam():
    #    return 1

    lam = 1

    def beta():
        return 0 # S_1[1:-1]*I_1[1:-1]/R_1[1:-1] 
    
    print S_1[1:-1]
    for n in range(1,Nt+1):
        S[1:-1] = S_1[1:-1] + dt*(-S_1[1:-1]*I_1[1:-1]+beta()*R_1[1:-1]+(S_1[2:]-2*S_1[1:-1]+S_1[:-2])/dx**2+f(t[n-1],x))
        I[1:-1] = I_1[1:-1] + dt*(S_1[1:-1]*I_1[1:-1]-lam*I_1[1:-1]+(I_1[2:]-2*I_1[1:-1]+I_1[:-2])/dx**2+g(t[n-1],x))
        R[1:-1] = R_1[1:-1] + dt*(lam*I_1[1:-1]-beta()*R_1[1:-1]+(R_1[2:]-2*R_1[1:-1]+R_1[:-2])/dx**2+h(t[n-1],x))
        """
        z[n] = z_X-n*dt
        z_S[n] = S[z_i]
        z_I[n] = I[z_i]
        z_R[n] = R[z_i]
        """
        S[0] = S[2]
        S[-1] = S[-3]
        I[0] = I[2]
        I[-1] = I[-3]
        R[0] = R[2]
        R[-1] =R[-3]
        if (n%40 == 0):
            np.save("images/Sub%04d" % (n/40),S)
            np.save("images/Inf%04d" % (n/40),I)
            np.save("images/Rem%04d" % (n/40),R)

        S_1[:] = S
        I_1[:] = I 
        R_1[:] = R
        
        
        #print "n",n,S[1:-1]
        

    #Find area of Infective
    #classnames = ['Susceptible', 'Infective','Removed']
    #z_list = [z_S,z_I,z_R] 
    #trav_wave(Nt,z,z_list,classnames,z_X,'1D')
    

    plotnames = ['images/Sub', 'images/Inf', 'images/Rem']
    moviename = 'plots/Travelling_wave'
    parameter_values = ['Sub','Inf','Rem']
    para_name = "Class"
    L = X

    return t,x,S[1:-1],I[1:-1],R[1:-1]


def build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X):
    x_list = []
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x = np.linspace(0,L,len_x)
        x_list.append(x)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    for j in range(Nt):
        for i in range(len(plotnames)):
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            plt.plot(x_list[i],np.load(img),label=label_name)
        plt.plot([z_X,z_X],[-0.1,1.1],'k')
        plt.text(z_X,-0.2,"x")
        plt.axis([0,L,-0.1,1.1])
        #plt.legend(loc=3)
        #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
        #plt.suptitle(moviename)
        nt = (float(T)/Nt)*j
        plt.title("time = %1.1f, z=%1.1f" % (nt,(z_X-nt)))
        plt.savefig("tmp%04d.png" % j)
        if(j%25 == 0 and j < 100):
            print j
            plt.savefig("plots/trav_wave%04d.png" % (j/25))
        plt.close()

    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
    for filename in glob.glob('tmp*.png'):
        os.remove(filename)

def add_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X):
    x_list = []
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x = np.linspace(0,L,len_x)
        x_list.append(x)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    fc = ['green','red']
    for j in range(Nt):
        for i in range(len(plotnames)):
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            if i == 0:
                load_val = np.load(img)
                plt.plot(x_list[i],load_val,label=label_name)
                plt.fill_between(x_list[i],0,load_val)
            else:
                load_val += np.load(img)
        plt.plot(x_list[i],load_val,label=label_name)
        plt.fill_between(x_list[i],load_val-np.load(img),load_val,facecolor=fc[i-1])
        plt.axis([0,L,0,1.2])
        plt.legend(loc=3)
        plt.suptitle(moviename)
        plt.title("Spatial spread")
        plt.savefig("tmp%04d.png" % j)
        plt.close()

    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
    for filename in glob.glob('tmp*.png'):
        os.remove(filename)


#build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X)
#os.system('rm images/*')
#plt.plot(r,I_1)
#plt.plot(r,S_1)
#plt.show()
