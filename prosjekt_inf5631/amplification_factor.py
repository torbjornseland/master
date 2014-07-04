import numpy as np
import matplotlib.pyplot as plt

def A_fe(dt):
    return 1-dt*a

def A_be(dt):
    return 1./(1+dt*a)

def exact(dt):
    return np.exp(-a*dt)

a = 1
dt_list = np.linspace(0,3,20)

fe = A_fe(dt_list) 
be = A_be(dt_list) 
u_e = exact(dt_list) 

plt.plot(dt_list,fe,label="Forward Euler")
plt.plot(dt_list,be,label="Backward Euler")
plt.plot(dt_list,u_e,label="Exact solution")
plt.xlabel("a*dt")
plt.ylabel("Amplification factor")
#ax = plt.gca()
#ax.invert_xaxis()
plt.legend()
plt.savefig("images/amplification_factor.png")
plt.show()

