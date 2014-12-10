import numpy as np
import matplotlib.pyplot as plt

T = 15
Nt = 15000
t = np.linspace(0,T,Nt+1)
#Random walk

susceptible_matrix = np.load("data/susceptible_matrix.npy")
infected_matrix = np.load("data/infected_matrix.npy")
removed_matrix = np.load("data/removed_matrix.npy")

susceptible_mean = np.zeros(Nt+1)
infected_mean = np.zeros(Nt+1)
removed_mean = np.zeros(Nt+1)

susceptible_sd = np.zeros(Nt+1)
infected_sd = np.zeros(Nt+1)
removed_sd = np.zeros(Nt+1)

success_plot = []
zero_plot = 0
for i in range(100):
    if (infected_matrix[i,7000] != 0):
        success_plot.append(i)
    else:
        zero_plot += 1

succ_size = len(success_plot)
print "succ_size", succ_size
s_susceptible_matrix = np.zeros([succ_size,Nt+1])
s_infected_matrix = np.zeros([succ_size,Nt+1])
s_removed_matrix = np.zeros([succ_size,Nt+1])
for i in range(succ_size):
    s_susceptible_matrix[i,:] = susceptible_matrix[success_plot[i],:]
    s_infected_matrix[i,:] = infected_matrix[success_plot[i],:]
    s_removed_matrix[i,:] = removed_matrix[success_plot[i],:]


for i in range(Nt+1):
        susceptible_mean[i] = np.mean(s_susceptible_matrix[:,i])
        infected_mean[i] = np.mean(s_infected_matrix[:,i])
        removed_mean[i] = np.mean(s_removed_matrix[:,i])

        susceptible_sd[i] = np.std(s_susceptible_matrix[:,i])
        infected_sd[i] = np.std(s_infected_matrix[:,i])
        removed_sd[i] = np.std(s_removed_matrix[:,i])


#plt.errorbar(t[::1500], susceptible_mean[::1500],susceptible_sd[::1500],color='blue', linestyle='None', marker='o')
#plt.errorbar(t[500::1500], infected_mean[500::1500],infected_sd[500::1500],color='green', linestyle='None', marker='o')
#plt.errorbar(t[1000::1500], removed_mean[1500::1500],removed_sd[1500::1500],color='red', linestyle='None', marker='o')

#plt.axis([0,T,0,800])
#plt.xlabel("Days")
#plt.ylabel("Number of boys")
#plt.title("Random walk vs ODE")
#plt.legend()
#plt.savefig("plots/English_boarding_random_ODE")
#plt.show()


#ODE equation

S_0 = 762
I_0 = 1
R_0 = 0


rho = 202
r = 2.18*10**(-3)
a = r*rho
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
#plt.plot(t,S,'b',label='Susceptible ODE')
#plt.plot(t,I,'g',label='Infected ODE')
#plt.plot(t,R,'r',label='Removed ODE')
#plt.plot(t, susceptible_mean, lw=1, label='Susceptible random', color='blue', ls='--') 
#plt.fill_between(t, susceptible_mean-susceptible_sd, susceptible_mean+susceptible_sd, facecolor='blue', alpha=0.1,
#                label='Standard deviation Sus.')
#plt.plot(t, infected_mean, lw=1, label='Infected random', color='green', ls='--') 
#plt.fill_between(t, infected_mean-infected_sd, infected_mean+infected_sd, facecolor='green', alpha=0.1,
#                label='Standard deviation Inf.')
#plt.plot(t, removed_mean, lw=1, label='Removed random', color='red', ls='--') 
#plt.fill_between(t, removed_mean-removed_sd, removed_mean+removed_sd, facecolor='red', alpha=0.1,
#                label='Standard deviation Rem.')
#plt.axis([0,T,0,800])
#plt.xlabel("Days")
#plt.ylabel("Number of boys")
##plt.title("Random walk vs ODE")
#plt.legend()
#plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
##plt.savefig("plots/English_boarding_random_ODE")
#plt.show()

