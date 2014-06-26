import numpy as np
import matplotlib.pyplot as plt

L = 3
Nx = 10
x = np.linspace(0.001,L,Nx+1)

def stab(x):
    return k*(4./x**2)*(np.sin(f*x/2.)**2)

k = f = 1
y = stab(x)
k = 2
y2 = stab(x)
k = 1
f = 2
y3 = stab(x)


plt.plot(x,y,label="dx,k=1,f=1")
plt.plot(x,y2,label="dx,k=2,f=1")
plt.plot(x,y3,label="dx,k=1,f=2")
#plt.axis([0,L,-0.2,1.2])
plt.legend()
plt.title("g(dx)=(k*4/dx^2)*sin(f*dx/2)^2")
plt.ylabel("g(dx)")
plt.xlabel("dx")
plt.savefig("images/Stability.png")
plt.close()
