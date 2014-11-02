from math import exp
import numpy as np
import matplotlib.pyplot as plt

def omega(t, a, sigma, T):
    return a*sum(exp(-0.5*(t-T[i])**2/sigma) for i in range(len(T)))

def run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0,D,mu, phases, ph_print):

    dt = 0.001
    #D = 30
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
    S[0] = S_0
    I[0] = I_0
    Z[0] = Z_0
    R[0] = R_0
    # step equations forward in time:
    if phases:
        for i in range(n):
            t = i*dt
            for j in range(len(phases)):
                if t < phases[j]:
                    val = j
                    break
            omega_t = omega(t, a, sigma, attacks)
            S[i+1] = S[i] + dt*(Sigma - (beta[val]+mu*omega_t)*S[i]*Z[i] - delta_S*S[i])
            I[i+1] = I[i] + dt*((beta[val]+ mu*omega_t)*S[i]*Z[i] - rho[val]*I[i] - delta_I*I[i])
            Z[i+1] = Z[i] + dt*(rho[val]*I[i] - (alpha[val] + omega_t)*S[i]*Z[i] + zeta*R[i])
            R[i+1] = R[i] + dt*(delta_S*S[i] - zeta*R[i] + delta_I*I[i] + (alpha[val] + omega_t)*S[i]*Z[i])
    else:
        for i in range(n):
            t = i*dt
            omega_t = omega(t, a, sigma, attacks)
            S[i+1] = S[i] + dt*(Sigma - (beta+mu*omega_t)*S[i]*Z[i] - delta_S*S[i])
            I[i+1] = I[i] + dt*((beta+ mu*omega_t)*S[i]*Z[i] - rho*I[i] - delta_I*I[i])
            Z[i+1] = Z[i] + dt*(rho*I[i] - (alpha + omega_t)*S[i]*Z[i] + zeta*R[i])
            R[i+1] = R[i] + dt*(delta_S*S[i] - zeta*R[i] + delta_I*I[i] + (alpha + omega_t)*S[i]*Z[i])

    if plot:
        plt.plot(T_tot,S,label="S")
        plt.plot(T_tot,I,label="I")
        plt.plot(T_tot,Z,label="Z")
        plt.plot(T_tot,R,label="R")
        plt.axis([0,D,0,800])
        plt.xlabel("days")
        plt.ylabel("humans")
        plt.legend()
        plt.savefig(filename)
        plt.show()
    if print_:
        ph_list = []
        for p in ph_print:
            ph_list.append(int(p/dt))
        for i in ph_list:
            print "---------------------"
            print "time, %f" % (i*dt)
            print "S_n",S[i]
            print "I_n",I[i]
            print "Z_n",Z[i]
            print "R_n",R[i]
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
    
    Sigma = 3.45*10**(-5) ;beta = 0.01155; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.37;zeta = 0
    alpha = 0.00044;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_initial_2.png"; plot = True;print_= True
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_)
    
    Sigma = 3.45*10**(-5) ;beta = 0.000011; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.5;zeta = 0
    alpha = 0.000208;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_hysterical_1.png"; 
    plot = True;print_= True; S_0 = 71.3; I_0 = 230.0; Z_0 = 298.9; R_0 = 21
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0)
    
    Sigma = 3.45*10**(-5) ;beta = 0.000011; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.5;zeta = 0
    alpha = 0.000208;a = 0.00103;sigma = 0.005;attacks = [0.625];filename = "plots/WD_zombie_counter_1.png"; 
    plot = True;print_= True; S_0 = 62; I_0 = 1; Z_0 = 359; R_0 = 200; D = 1, mu = 4./30
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0,D)
    
    Sigma = 3.45*10**(-5) ;beta = 0.000011; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.5;zeta = 0
    alpha = 0.000208;a = 0.0073;sigma = 0.005;attacks = [0.625];filename = "plots/WD_zombie_counter_2.png"; 
    plot = True;print_= True; S_0 = 62; I_0 = 1; Z_0 = 359; R_0 = 200; D = 1; mu = 0.14
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0,D,mu)
    
    Sigma = 3.45*10**(-5) ;beta = 0.000011; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = 1.5;zeta = 0
    alpha = 0.000208;a = 0.0073;sigma = 0.005;filename = "plots/WD_zombie_counter_series.png"; 
    plot = True;print_= True; S_0 = 62; I_0 = 1; Z_0 = 359; R_0 = 200; D = 200; mu = 0.14
    attacks = []
    for i in range(100):
        attacks.append(i*2)
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0,D,mu)
    """
    Sigma = 3.45*10**(-5) ;beta = [0.01155, 0.000011]; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = [1.37,1.5] ;zeta = 0
    alpha = [0.00044,0.000208];a = 0.0073; sigma = 0.005;filename = "plots/WD_zombie_all_phases_2.png"; 
    plot = True;print_= True; S_0 = 621; I_0 = 0; Z_0 = 1; R_0 = 0; D = 34; mu = 0.14; attacks = [33.125]; phases = [3,34]; 
    ph_print = [0,3,33,34]
    run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0,D,mu,phases, ph_print)
    """
    def check_param(beta_list,rho_list,alpha_list,nr, title):
        S_n_list = []
        R_n_list = []

        for i in beta_list:
            for k in rho_list:
                for j in alpha_list:
                    Sigma = 3.45*10**(-5) ;beta = i; delta_S = 2.5*10**(-5);delta_I = delta_S ;rho = k;zeta = 0
                    alpha = j;a = 0;sigma = 0.5;attacks = [5, 10, 18];filename = "plots/WD_zombie_initial_2.png"
                    S_0 = 71.3; I_0 = 230.0; Z_0 = 298.9; R_0 = 21;plot=False;print_ = False
                    S_n,R_n = run_program(Sigma,beta,delta_S,delta_I,rho,zeta,alpha,a,sigma,attacks,filename,plot,print_,S_0,I_0,Z_0,R_0)
                    if(S_n < 63 and S_n > 61) and (R_n < 201 and R_n> 199):
                        print "beta = %f,rho=%f, alpha=%f, S_n = %f, R_n 0 %f" % (i,k,j,S_n,R_n)
                    S_n_list.append(S_n)
                    R_n_list.append(R_n)
        plt.subplot(2,2,nr)
        plt.plot(S_n_list, R_n_list, 'ro',label= "data from variable")
        plt.plot([62], [200], 'bo',label= "exact data")
        plt.axis([60,63,190,204])
        plt.xlabel("susceptible")
        plt.ylabel("removed")
        plt.legend()
        plt.title(title)
    
    
    beta_list = np.linspace(0.00001,0.000012,5)
    rho_list = np.linspace(0.5,2,4)
    alpha_list = np.linspace(0.0002,0.00021,5)
    
    beta_list_1 = [0.000011]#np.linspace(0.,0.5,100)
    rho_list_1 = [1.5]#np.linspace(0.5,2,20)
    alpha_list_1 = [0.000208]#np.linspace(0.01,0.15,20)
    
    check_param(beta_list,rho_list_1,alpha_list_1,1,"beta = [0.01,0.013]")
    check_param(beta_list_1,rho_list,alpha_list_1,2,"varrho = [1.2,1.6]")
    check_param(beta_list_1,rho_list_1,alpha_list,3,"alpha = [0.0003, 0.0007]")
    check_param(beta_list,rho_list,alpha_list,4,"All parameters")
    
    #plt.savefig("plots/check_parameters_hysterical_2.png")
    plt.show()
     
    t = np.linspace(0,0.25,101)
    y = np.zeros(101)
    a = 0.00103
    sigma_list = [0.005]#,0.5,0.8]
    T = [0.125]
    for sigma in sigma_list:
        area = 0
        for i in range(101):
            y[i] = omega(t[i], a, sigma, T)
            area += y[i]
        plt.plot(t,y,label="sigma=%s" %sigma)
        area = area*(2./101)
        print area
    #plt.legend()
    plt.title("a=0.9,T=1,sigma=0.1")
    #plt.savefig("omega_function.png")
    plt.show()
    """
