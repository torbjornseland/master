import numpy as np
import matplotlib.pyplot as plt

#Test diffusion
#model 1: Ordinary diffusion constant
def model1():
	return S_1_1[1:-1] + dt*D_s*((S_1_1[:-2]-2*S_1_1[1:-1]+S_1_1[2:])/dx**2)

#Model 2: Spatial dependent diffusion constant
def model2():
	return S_1_2[1:-1] + dt*gamma_s[1:-1]*((S_1_2[:-2]-2*S_1_2[1:-1]+S_1_2[2:])/dx**2)

#Model 3: Spatial derivative dependent diffusion
def model3():
	return S_1_3[1:-1] + (dt/(2*dx**2))*((gamma_s[2:]+gamma_s[1:-1])*(S_1_3[2:]-S_1_3[1:-1])-(gamma_s[:-2]+gamma_s[1:-1])*(S_1_3[1:-1]-S_1_3[:-2]))

Nx = 100
dt = 0.001
dx = 0.1

S1 = np.zeros([Nx+3])   #list of Susceptible
S2 = np.zeros([Nx+3])   #list of Susceptible
S3 = np.zeros([Nx+3])   #list of Susceptible

x = np.linspace(0,1,Nx+1)

S_1_1 = np.linspace(1,0,Nx+3)  #list of Susceptible in previous time step
S_1_2 = np.linspace(1,0,Nx+3)  #list of Susceptible in previous time step
S_1_3 = np.linspace(1,0,Nx+3)  #list of Susceptible in previous time step

D_s = 0
#gamma_s = np.linspace(0,5,Nx+3)
#gamma_s = np.linspace(1,0,Nx+3)
gamma_s = np.ones(Nx+3)*2
#gamma_s[:Nx/8] = gamma_s[:Nx/8]*0
#gamma_s[-Nx/8:] = gamma_s[-Nx/8:]*0
#gamma_s[3*Nx/8:-3*Nx/8] = gamma_s[3*Nx/8:-3*Nx/8]*0

for i in range(10000):
	S1[1:-1] = model1()	   
	S2[1:-1] = model2()	   
	S3[1:-1] = model3()	   

	S1[0] = S1[2]
	S2[0] = S2[2]
	S3[0] = S3[2]
	
	S1[-1] = S1[-3]	
	S2[-1] = S2[-3]	
	S3[-1] = S3[-3]	
	
	print "S",S3[-2]	

	S_1_1[:] = S1
	S_1_2[:] = S2
	S_1_3[:] = S3


plt.plot(x,S1[1:-1],label="model1")
plt.plot(x,S2[1:-1],label="model2")
plt.plot(x,S3[1:-1],label="model3")
plt.legend()
plt.show()
