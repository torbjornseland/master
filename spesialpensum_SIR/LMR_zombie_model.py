from math import exp
import numpy as np
import matplotlib.pyplot as plt

def run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_):
    def omega(t, a, sigma, T):
        return a*sum(exp(-0.5*(t-T[i])**2/sigma) for i in range(len(T)))

    dt = 0.001
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
    S[0] = 621
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

    if plot:
        plt.plot(T_tot,S,label="S")
        plt.plot(T_tot,I,label="I")
        plt.plot(T_tot,Z,label="Z")
        plt.plot(T_tot,R,label="R")
        plt.axis([0,3,0,800])
        plt.xlabel("days")
        plt.ylabel("humans")
        plt.legend()
        #plt.savefig(filename)
        plt.show()
    if print_:
        print "S_n",S[n]
        print "I_n",I[n]
        print "Z_n",Z[n]
        print "R_n",R[n]
    return S[n],R[n]

if __name__ == "__main__":
    """
    Sigma = 0;beta = 0.0625;delta_S = 0;delta_I = 0;rho = 1;zeta = 0
    alpha = 0;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/LMR_zombie_initial_1.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
    
    Sigma = 20;beta = 0.03;delta_S = 0;delta_I = 0;rho = 1;zeta = 0
    alpha = 0;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/LMR_zombie_initial_2.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
    Sigma = 3.45*10**(-5) ;beta = 0.3; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1;zeta = 0
    alpha = 0.;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_initial_1.png"
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename)
    """
    Sigma = 3.45*10**(-5) ;beta = 0.01155; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.37;zeta = 0
    alpha = 0.00044;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_initial_2.png"; plot = True;print_= True
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_)
    """
    def check_param(beta_list,rho_list,alpha_list,nr, title):
        S_n_list = []
        R_n_list = []

        for i in beta_list:
            for k in rho_list:
                for j in alpha_list:
                    Sigma = 3.45*10**(-5) ;beta = i; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = k;zeta = 0
                    alpha = j;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_initial_2.png"
                    S_n,R_n = run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot=False,print_=False)
                    if(S_n < 73 and S_n > 69) and (R_n < 22 and R_n> 18):
                        print i,k,j
                    S_n_list.append(S_n)
                    R_n_list.append(R_n)
        plt.subplot(2,2,nr)
        plt.plot(S_n_list, R_n_list, 'ro',label= "data from variable")
        plt.plot([71], [20], 'bo',label= "exact data")
        plt.axis([0,300,0,50])
        plt.xlabel("susceptible")
        plt.ylabel("removed")
        plt.legend()
        plt.title(title)
    
    
    beta_list = np.linspace(0.010,0.013,5)
    rho_list = [1.37]#np.linspace(0.5,2,20)
    alpha_list = [0.00044]#np.linspace(0.01,0.15,20)
    nr = 1
    check_param(beta_list,rho_list,alpha_list,nr,"beta = [0.01,0.013]")
    
    beta_list = [0.01155]#np.linspace(0.,0.5,100)
    rho_list = np.linspace(1.2,1.6,5)
    alpha_list = [0.00044]#np.linspace(0.01,0.15,20)
    nr = 2
    check_param(beta_list,rho_list,alpha_list,nr,"varrho = [1.2,1.6]")
    
    beta_list = [0.01155]#np.linspace(0.,0.5,100)
    rho_list = [1.37]#np.linspace(0.5,2,20)
    alpha_list = np.linspace(0.0003,0.0007,5)
    nr = 3
    check_param(beta_list,rho_list,alpha_list,nr,"alpha = [0.0003, 0.0007]")
    
    beta_list = np.linspace(0.010,0.013,5)
    rho_list = np.linspace(1.2,1.6,5)
    alpha_list = np.linspace(0.0003,0.0007,5)
    nr = 4
    check_param(beta_list,rho_list,alpha_list,nr,"All parameters")
    
    plt.savefig("check_parameters.png")
    plt.show()
    """
    
