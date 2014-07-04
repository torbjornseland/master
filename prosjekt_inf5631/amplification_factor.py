import matplotlib.pyplot as plt

def A_fe(dt):
    return 1+dt*a

def A_be(dt):
    return 1./(1-dt*a)

a = 1
dt_list = [0.9,0.8,0.65,0.5,0.25,0.1,0.05,0.01,0.005,0.001]

fe = []
be = []
for i in dt_list:
    fe.append(A_fe(i))
    be.append(A_be(i))

plt.plot(dt_list,fe,label="Forward Euler")
plt.plot(dt_list,be,label="Backward Euler")
plt.xlabel("a*dt")
plt.ylabel("Amplification factor")
ax = plt.gca()
ax.invert_xaxis()
plt.legend()
plt.savefig("images/amplification_factor.png")
plt.show()

