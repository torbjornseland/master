import numpy as np
import matplotlib.pyplot as plt

T = 34
Nt = 3400
t = np.linspace(0,T,Nt+1)
#Random walk
savename = "three_phases"
N = 50


susceptible_matrix = np.load("data/susceptible_matrix_%s.npy" % savename)
infected_matrix = np.load("data/infected_matrix_%s.npy" % savename)
zombie_matrix = np.load("data/zombie_matrix_%s.npy" % savename)
removed_matrix = np.load("data/removed_matrix_%s.npy" % savename)

S = np.load("data/ODE_three_phases_sus.npy")
I = np.load("data/ODE_three_phases_inf.npy")
Z = np.load("data/ODE_three_phases_zom.npy")
R = np.load("data/ODE_three_phases_rem.npy")

print susceptible_matrix

susceptible_mean = np.zeros(Nt+1)
infected_mean = np.zeros(Nt+1)
zombie_mean = np.zeros(Nt+1)
removed_mean = np.zeros(Nt+1)

susceptible_sd = np.zeros(Nt+1)
infected_sd = np.zeros(Nt+1)
zombie_sd = np.zeros(Nt+1)
removed_sd = np.zeros(Nt+1)

success_plot = []
zero_plot = 0
for i in range(N):
    if (zombie_matrix[i,500] != 0):
        success_plot.append(i)
    else:
        zero_plot += 1

succ_size = len(success_plot)
print "succ_size", succ_size
s_susceptible_matrix = np.zeros([succ_size,Nt+1])
s_infected_matrix = np.zeros([succ_size,Nt+1])
s_zombie_matrix = np.zeros([succ_size,Nt+1])
s_removed_matrix = np.zeros([succ_size,Nt+1])
for i in range(succ_size):
    s_susceptible_matrix[i,:] = susceptible_matrix[success_plot[i],:]
    s_infected_matrix[i,:] = infected_matrix[success_plot[i],:]
    s_zombie_matrix[i,:] = zombie_matrix[success_plot[i],:]
    s_removed_matrix[i,:] = removed_matrix[success_plot[i],:]


for i in range(Nt+1):
        susceptible_mean[i] = np.mean(s_susceptible_matrix[:,i])
        infected_mean[i] = np.mean(s_infected_matrix[:,i])
        zombie_mean[i] = np.mean(s_zombie_matrix[:,i])
        removed_mean[i] = np.mean(s_removed_matrix[:,i])

        susceptible_sd[i] = np.std(s_susceptible_matrix[:,i])
        infected_sd[i] = np.std(s_infected_matrix[:,i])
        zombie_sd[i] = np.std(s_zombie_matrix[:,i])
        removed_sd[i] = np.std(s_removed_matrix[:,i])

for i in [300,3300,3400]:
        print "susc",susceptible_mean[i]
        print "inf",infected_mean[i]
        print "zom",zombie_mean[i]
        print "rem",removed_mean[i]

        print "ODE susc",S[i]
        print "ODE inf",I[i]
        print "ODE zom",Z[i]
        print "ODE rem",R[i]
        

#plt.errorbar(t[::200], susceptible_mean[::200],susceptible_sd[::200],color='blue', linestyle='None', marker='o')
#plt.errorbar(t[100::200], infected_mean[100::200],infected_sd[100::200],color='green', linestyle='None', marker='o')
#plt.errorbar(t[::200], zombie_mean[::200],zombie_sd[::200],color='red', linestyle='None', marker='o')
#plt.errorbar(t[100::200], removed_mean[100::200],removed_sd[100::200],color='m', linestyle='None', marker='o')

#plt.axis([0,T,0,800])
#plt.xlabel("Days")
#plt.ylabel("Number of boys")
#plt.title("Random walk vs ODE")
#plt.legend()
#plt.savefig("plots/English_boarding_random_ODE")
#plt.show()


#ODE equation
"""
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
"""


plt.plot(t,S,'b',label='Susceptible ODE')
plt.plot(t,I,'g',label='Infected ODE')
plt.plot(t,Z,'r',label='Infected ODE')
plt.plot(t,R,'c',label='Removed ODE')

#plt.plot(t, susceptible_mean, lw=1, label='Susceptible moving smart', color='blue', ls='--') 
plt.fill_between(t, susceptible_mean-susceptible_sd, susceptible_mean+susceptible_sd, facecolor='blue', alpha=0.1,
                label='Standard deviation Sus.')
#plt.plot(t, infected_mean, lw=1, label='Infected moving smart', color='green', ls='--') 
plt.fill_between(t, infected_mean-infected_sd, infected_mean+infected_sd, facecolor='green', alpha=0.1,
                label='Standard deviation Inf.')
#plt.plot(t, zombie_mean, lw=1, label='Zombie moving smart', color='red', ls='--') 
plt.fill_between(t, zombie_mean-zombie_sd, zombie_mean+zombie_sd, facecolor='red', alpha=0.1,
                label='Standard deviation Zom.')
#plt.plot(t, removed_mean, lw=1, label='Removed moving smart', color='c', ls='--') 
plt.fill_between(t, removed_mean-removed_sd, removed_mean+removed_sd, facecolor='c', alpha=0.1,
                label='Standard deviation Rem.')
plt.axis([0,T,0,800])
plt.xlabel("Minutes")
plt.ylabel("Number")
#plt.title("Random walk at Frederikkeplassen")
plt.legend()
plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
#plt.savefig("../plots/Random_three_phases")
plt.show()
