import numpy as np



def volume_engine(z_mat,size):
    volume = ((z_mat[:-1,:-1]+z_mat[:-1,1:]+z_mat[1:,:-1]+z_mat[1:,1:])/float(4))*size
    print volume
    return volume.sum()


a = np.ones([11,11])
a = a*np.linspace(0,1,11)
si = 1

print volume_engine(a,si)
