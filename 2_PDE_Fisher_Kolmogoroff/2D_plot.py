from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import numpy as np

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
X, Y, Z = axes3d.get_test_data(0.05)
#ax.plot_wireframe(X, Y, Z, rstride=10, cstride=10)
#ax.plot_wireframe([1,2,3],[1,2,3],[[1,2,3],[3,4,5],[3,5,3]], rstride=1, cstride=1)
print X
plt.show()

