import glob,os
import numpy as np
import matplotlib.pyplot as plt

T = 40
Nx = 100
Nt = 4000
X = 20
lam = 0.5

S = np.zeros(Nx+1)   #list of Susceptible
S_1 = np.ones(Nx+1)#list of Susceptible in previous time step
I = np.zeros(Nx+1)   #list of Susceptible
I_1 = np.zeros(Nx+1)#list of Susceptible in previous time step
R = np.zeros(Nx+1)   #list of Susceptible
R_1 = np.zeros(Nx+1)#list of Susceptible in previous time step

x = np.linspace(0,X,Nx+1)
t = np.linspace(0,T,Nt+1)

dt = t[1]-t[0]
dx = x[1]-x[0]

#Check travelling wave
z = np.zeros(Nt+1)
z_S = np.zeros(Nt+1)
z_I = np.zeros(Nt+1)
z_R = np.zeros(Nt+1)
z_X = 15
z_i = int(z_X/dx)

def gauss(t,a,sigma,T):
    return a*np.exp(-0.5*(t-T)**2/sigma)

I_1[:] = gauss(x,0.2,0.5,0) #starts with a gauss function
#I_1[:] += 0.1

np.save("images/Sub%04d" % 0,S_1) #initial conditions
np.save("images/Inf%04d" % 0,I_1) #initial conditions
np.save("images/Rem%04d" % 0,R_1) #initial conditions

#Initial cond for travelling wave
z[0] = z_X
z_S[0] = S_1[z_i]
z_I[0] = I_1[z_i]
z_R[0] = R_1[z_i]


for n in range(1,Nt+1):
    S[1:-1] = S_1[1:-1] + dt*(-S_1[1:-1]*I_1[1:-1]+(S_1[2:]-2*S_1[1:-1]+S_1[:-2])/dx**2)
    I[1:-1] = I_1[1:-1] + dt*(S_1[1:-1]*I_1[1:-1]-lam*I_1[1:-1]+(I_1[2:]-2*I_1[1:-1]+I_1[:-2])/dx**2)
    R[1:-1] = R_1[1:-1] + dt*(lam*I_1[1:-1]+(R_1[2:]-2*R_1[1:-1]+R_1[:-2])/dx**2)

    z[n] = z_X-n*dt
    z_S[n] = S[z_i]
    z_I[n] = I[z_i]
    z_R[n] = R[z_i]

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

plt.plot(z,z_S,label="Susceptible")
plt.plot(z,z_I,label="Infective")
plt.plot(z,z_R,label="Removed")
plt.xlabel("z")
plt.axis([z_X-40,z_X,0,1])
plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
plt.savefig("plots/epidemic_wave_z_lambda_0_5.png")
plt.close()
#plt.show()

plotnames = ['images/Sub', 'images/Inf', 'images/Rem']
moviename = 'plots/Travelling_wave'
parameter_values = ['Sub','Inf','Rem']
para_name = "Class"
L = X

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


build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X)
os.system('rm images/*')
#plt.plot(r,I_1)
#plt.plot(r,S_1)
#plt.show()
