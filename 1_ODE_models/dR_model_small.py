import numpy as np
import matplotlib.pyplot as plt

Nt = 100
T = 30
t = np.linspace(0,T,Nt+1)
dt = t[1]-t[0]
R_list = np.zeros(Nt+1)
t_2 = np.linspace(0,T,T+1)
BP_data = [2,3,5,10,20,30,40,50,80,100,200,300,400,500,600,700,800,900,800,700,600,500,400,300,200,100,80,50,40,30,20]

for i in range(Nt):
    t_ = 0.2*t[i+1]-3.4
    R_list[i+1] = 890*(2*np.cosh(t_)/(np.cosh(2*t_)+1))**2


plt.plot(t,R_list)
plt.plot(t[::10],R_list[::10],'bo',label='Kermack and McKendrick')
print len(t_2)
print len(BP_data)
plt.plot(t_2,BP_data,'ro',label='Correct data from BP')
#plt.axis([0,N,0,N])
plt.xlabel("Weeks")
plt.ylabel("Deaths")
plt.title("Bombay Plague Epidemic")
plt.legend()
plt.savefig("plots/Bombay_plague.png")
plt.show()




