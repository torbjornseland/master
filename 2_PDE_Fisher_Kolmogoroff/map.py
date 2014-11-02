from pylab import *
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.cbook import get_sample_data
from matplotlib._png import read_png
fn = get_sample_data("Blindern.png",asfileobj=True)
img = read_png(fn)
x, y = ogrid[0:img.shape[0], 0:img.shape[1]]

ax = gca(projection='3d')
#ax.plot_surface(x, y, 0, rstride=10, cstride=10, facecolors=img)
ax.set_xlim3d(0,x[-1][0])
ax.set_ylim3d(0,y[0][-1])
ax.set_zlim3d(0,0.1)

#show()
