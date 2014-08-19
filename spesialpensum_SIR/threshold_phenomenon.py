import numpy as np
import matplotlib.pyplot as plt


#Initial conditions
N = 100
r = 0.02
a = 0.7
rho = a/r

plt.plot([N,0],[0,N],label="Possible startposition")
plt.plot([rho,rho],[0,N-rho],label="Threshold value")
S0_list = [100,90,80]#,70,60,50,40,30,20]
for j in S0_list:
    S_0 = j
    I_0 = N-S_0
    R_0 = 0

    T = 10
    Nt = 1000

    t = np.linspace(0,T,Nt+1)
    dt = t[1]-t[0]
    S = np.zeros(Nt+1)
    I = np.zeros(Nt+1)
    R = np.zeros(Nt+1)

    S[0] = S_0
    I[0] = I_0
    R[0] = R_0

    print "round"
    for i in range(Nt):
        S[i+1] = S[i] - dt*r*S[i]*I[i] 
        I[i+1] = I[i] + dt*(r*S[i]*I[i]-a*I[i])
        R[i+1] = R[i] + dt*a*I[i]
        if(I[i]>I[i+1] and I[i]>I[i-1]):
            print "max",I[i]
        #print "constant",S[i+1]+I[i+1]-rho*np.log(S[i+1])



    plt.plot(S,I)
plt.axis([0,N,0,N])
plt.xlabel("S")
plt.ylabel("I")
plt.legend()
#plt.savefig("plots/threshold_phenomenon.png")
plt.show()




