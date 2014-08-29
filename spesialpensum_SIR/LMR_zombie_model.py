from math import exp
import numpy as np
import matplotlib.pyplot as plt

def run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename):
    def omega(t, a, sigma, T):
        return a*sum(exp(-0.5*(t-T[i])**2/sigma) for i in range(len(T)))

    dt = 0.01
    D = 3
    n = int(D/dt)
    T_tot = np.linspace(0,D,n+1)
    # time step measured in hours
    # simulation lasts for D days
    # corresponding total no of hours
    S = np.zeros(n+1)
    I = np.zeros(n+1)
    Z = np.zeros(n+1)
    R = np.zeros(n+1)
    # initial conditions:
    S[0] = 721
    I[0] = 0
    Z[0] = 1
    R[0] = 0
    # step equations forward in time:
    for i in range(n):
        t = i*dt
        omega_t = omega(t, a, sigma, attacks)
        S[i+1] = S[i] + dt*(Sigma - beta*S[i]*Z[i] - delta_S*S[i])
        I[i+1] = I[i] + dt*(beta*S[i]*Z[i] - rho*I[i] - delta_I*I[i])
        Z[i+1] = Z[i] + dt*(rho*I[i] - (alpha + omega_t)*S[i]*Z[i] + zeta*R[i])
        R[i+1] = R[i] + dt*(delta_S*S[i] - zeta*R[i] + delta_I*I[i] + (alpha + omega_t)*S[i]*Z[i])

    plt.plot(T_tot,S,label="S")
    plt.plot(T_tot,I,label="I")
    plt.plot(T_tot,Z,label="Z")
    plt.plot(T_tot,R,label="R")
    plt.axis([0,3,0,800])
    plt.xlabel("hours")
    plt.ylabel("humans")
    plt.legend()
    #plt.savefig(filename)
    plt.show()
    print "S_N",S[n]
    print "I_N",I[n]
    print "Z_N",Z[n]
    print "R_N",R[n]

if __name__ == "__main__":
    """
    Sigma = 0;beta = 0.0625;delta_S = 0;delta_I = 0;rho = 1;zeta = 0
    alpha = 0;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/LMR_zombie_initial_1.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
    
    Sigma = 20;beta = 0.03;delta_S = 0;delta_I = 0;rho = 1;zeta = 0
    alpha = 0;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/LMR_zombie_initial_2.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
    """
    Sigma = 0;beta = 0.3; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1;zeta = 0
    alpha = 0.11;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/LMR_zombie_initial_1.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
