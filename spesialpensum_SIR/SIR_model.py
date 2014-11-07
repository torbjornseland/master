import numpy as np
import matplotlib.pyplot as plt


#Initial conditions

N = 763
S_0 = 762
I_0 = N-S_0
R_0 = 0
rho_list = [202]#50,100,202,400]

for j in range(1):
    rho = rho_list[j]
    r = 2.18*10**(-3)
    a = r*rho
    T = 15
    Nt = 100000

    t = np.linspace(0,T,Nt+1)
    dt = t[1]-t[0]
    S = np.zeros(Nt+1)
    I = np.zeros(Nt+1)
    R = np.zeros(Nt+1)

    S[0] = S_0
    I[0] = I_0
    R[0] = R_0

    for i in range(Nt):
        S[i+1] = S[i] - dt*r*S[i]*I[i] 
        I[i+1] = I[i] + dt*(r*S[i]*I[i]-a*I[i])
        R[i+1] = R[i] + dt*a*I[i]


    #plt.subplot(2,2,j+1)
    plt.plot(t,S,label='susceptible')
    plt.plot(t,I,label='infective')
    plt.plot(t,R,label='removed')
    plt.axis([0,T,0,800])
    plt.xlabel("Days")
    plt.ylabel("Number of boys")
    plt.title("rho = %s" % rho_list[j])
    #plt.legend()
    #plt.savefig("plots/English_boarding_school_changes.png")
plt.show()

ch_list = [0,5,10,15]
dt = T/float(Nt)
for k in ch_list:
	k_c	= int(k/dt)
	print "k=",k_c*dt
	print "S",S[k_c] 
	print "I",I[k_c] 
	print "R",R[k_c] 




