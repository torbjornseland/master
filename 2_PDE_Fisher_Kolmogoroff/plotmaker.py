import numpy as np
import glob,os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d

def build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X):
    x_list = []
    y_list = []
    surf_color = ['blue','green','red']
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x,y = np.meshgrid(np.linspace(0,L,len_x),np.linspace(0,L,len_x))
        x_list.append(x)
        y_list.append(y)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    for j in range(Nt):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(len(plotnames)):
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            #plt.plot(x_list[i],np.load(img),label=label_name)
            ax.plot_wireframe(x_list[i],y_list[i],np.load(img)/(L**2), rstride=10, cstride=10,color=surf_color[i])
        #plt.plot([z_X,z_X],[-0.1,1.1],'k')
        #plt.text(z_X,-0.2,"x")
        #plt.axis([0,L,-0.1,1.1])
        ax.set_xlim3d(0,L)
        ax.set_ylim3d(0,L)
        ax.set_zlim3d(0,8)
        #plt.legend(loc=3)
        #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
        #plt.suptitle(moviename)
        nt = (float(T)/Nt)*j
        plt.title("time = %1.1f" % nt)
        plt.savefig("tmp%04d.png" % j)
        
        if(j%50 == 0 and j < 200):
            print j
            plt.savefig("plots/2D_gauss_wave%04d.png" % (j/50))
        
        plt.close()

    os.system('doconce combine_images plots/2D_gauss_wave000* %s_sub.png' % moviename)
    os.system('rm plots/2D_gauss_wave000*')
    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
    for filename in glob.glob('tmp*.png'):
        os.remove(filename)

def add_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X):
    x_list = []
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x = np.linspace(0,L,len_x)
        x_list.append(x)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    fc = ['green','red']
    for j in range(Nt):
        for i in range(len(plotnames)):
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            if i == 0:
                load_val = np.load(img)
                plt.plot(x_list[i],load_val,label=label_name)
                plt.fill_between(x_list[i],0,load_val)
            else:
                load_val += np.load(img)
        plt.plot(x_list[i],load_val,label=label_name)
        plt.fill_between(x_list[i],load_val-np.load(img),load_val,facecolor=fc[i-1])
        plt.axis([0,L,0,1.2])
        plt.legend(loc=3)
        plt.suptitle(moviename)
        plt.title("Spatial spread")
        plt.savefig("tmp%04d.png" % j)
        plt.close()

    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
    for filename in glob.glob('tmp*.png'):
        os.remove(filename)
        

def volume_engine(z_mat,size):
    volume = ((z_mat[:-1,:-1]+z_mat[:-1,1:]+z_mat[1:,:-1]+z_mat[1:,1:])/float(4))*size
    return volume.sum()

def plot_volume(t,S_vol,I_vol,R_vol,moviename,t_size=1,x_size=1):
    #btt = 1.66116
    x_size = 10*10
    plt.plot(t/t_size,S_vol/x_size)
    plt.plot(t/t_size,I_vol/x_size)
    plt.plot(t/t_size,R_vol/x_size)
    plt.axis([0,15,0,800])
    plt.xlabel('Days')
    plt.ylabel('Number of boys')
    plt.title('Boarding School modeled with uniformly mixed groups')
    plt.savefig('%s_number.png' % moviename)
    plt.show()
