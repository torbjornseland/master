import numpy as np
import glob,os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import axes3d
from matplotlib import cm
import matplotlib.image as mpimg

def build_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X,max_val,phases,phase_name):
    x_list = []
    y_list = []
    surf_color = ['blue','green','red','cyan']
    for i in plotnames:
        img = "%s%04d.npz" % (i,0)
	arr = np.load(img)
        len_x = len(arr['arr_0'])
        x,y = np.meshgrid(np.linspace(0,L,len_x),np.linspace(0,L,len_x))
        x_list.append(x)
        y_list.append(y)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    ph_check = []
    for ph in phases:
        if ph == T:
            ph_check.append(Nt-1)
        else:
            ph_check.append(int((Nt*ph)/T))

    print "ph_check", ph_check
    sub_num = int((Nt-1)/3)
    for j in range(Nt):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        for i in range(len(plotnames)):
            img = "%s%04d.npz" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
	    arr = np.load(img)
            #plt.plot(x_list[i],np.load(img),label=label_name)
            ax.plot_wireframe(x_list[i],y_list[i],arr['arr_0'], rstride=10, cstride=10,color=surf_color[i])
        #plt.plot([z_X,z_X],[-0.1,1.1],'k')
        #plt.text(z_X,-0.2,"x")
        #plt.axis([0,L,-0.1,1.1])
        ax.set_xlim3d(0,L)
        ax.set_ylim3d(0,L)
        ax.set_zlim3d(0,max_val*1.1)
        #plt.legend(loc=3)
        #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
        #plt.suptitle(moviename)
        nt = (float(T)/Nt)*j
        plt.title("time = %1.1f" % nt)
        plt.savefig("movie_images/tmp%04d.png" % j)
        
        for ph in range(len(ph_check)):
            if(j == ph_check[ph]):
                print "sub"
                print j,ph
                plt.title("%s, time=%2.1f" % (phase_name[ph],(j*T/float(Nt))))
                plt.savefig("plots/2D_gauss_wave%04d.png" % ph)
        
        plt.close()

    os.system('doconce combine_images plots/2D_gauss_wave000* %s_sub.png' % moviename)
    os.system('rm plots/2D_gauss_wave000*')
    #os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm -y' %('movie_images/tmp%04d.png',moviename))
    for filename in glob.glob('movie_images/tmp*.png'):
        os.remove(filename)

def sub_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X,max_val,classnames,phases,phase_name):
    x_list = []
    y_list = []
    surf_color = ['blue','green','red','cyan']
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x,y = np.meshgrid(np.linspace(0,L,len_x),np.linspace(0,L,len_x))
        x_list.append(x)
        y_list.append(y)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    #sub_num = int(Nt/3)
    ph_check = []
    for ph in phases:
        ph_check.append(int((Nt*ph)/T))
    
    for j in range(Nt):
        fig = plt.figure()
        for i in range(len(plotnames)):
            ax = fig.add_subplot(2,2,i+1,projection='3d')
            #ax.title("%s" % classnames[i])
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            #plt.plot(x_list[i],np.load(img),label=label_name)
            #ax.plot_wireframe(x_list[i],y_list[i],np.load(img), rstride=10, cstride=10,color=surf_color[i])
            surf = ax.plot_surface(x_list[i],y_list[i],np.load(img), rstride=5, cstride=5,cmap=cm.coolwarm,linewidth=0, antialiased=False,vmin=0,vmax=max_val)
            ax.set_title(classnames[i])
            ax.set_zlim(0,max_val)
            ax.set_xlim3d(0,L)
            ax.set_ylim3d(0,L)
            #ax.axes.xaxis.set_ticklabels([])
            #ax.axes.yaxis.set_ticklabels([])
            #ax.axes.zaxis.set_ticklabels([])
            #ax.set_xticks([
            #fig.colorbar(surf, shrink=0.5, aspect=5)
        #plt.plot([z_X,z_X],[-0.1,1.1],'k')
        #plt.text(z_X,-0.2,"x")
        #plt.axis([0,L,-0.1,1.1])
        #plt.legend(loc=3)
        #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
        #plt.suptitle(moviename)
        nt = (float(T)/Nt)*j
        #plt.title("time = %1.1f" % nt)
        fig.tight_layout()
        plt.savefig("movie_images/tmp_sub%04d.png" % j)
        
        for ph in range(len(ph_check)):
            if(j == ph_check[ph]):
                print "sub"
                print j,ph
                plt.suptitle(phase_name[ph])
                plt.savefig("plots/2D_gauss_wave%04d.png" % ph)
        
        plt.close()

    os.system('doconce combine_images plots/2D_gauss_wave000* %s_surface_sub.png' % moviename)
    os.system('rm plots/2D_gauss_wave000*')
    #os.system('avconv -r 10 -i %s -vcodec libvpx %s_surface.webm -y' %('movie_images/tmp_sub%04d.png',moviename))
    for filename in glob.glob('movie_images/tmp_sub*.png'):
        os.remove(filename)

def contourf_plot(plotnames,moviename,parameter_values,para_name,L,T,z_X,max_val,classnames):
    x_list = []
    y_list = []
    surf_color = ['blue','green','red','cyan']
    for i in plotnames:
        img = "%s%04d.npy" % (i,0)
        len_x = len(np.load(img))
        x,y = np.meshgrid(np.linspace(0,L,len_x),np.linspace(0,L,len_x))
        x_list.append(x)
        y_list.append(y)
    plotname = "%s*" %(plotnames[0])
    Nt = len(glob.glob(plotname))
    print Nt
    sub_num = int(Nt/3)
    origin = 'lower'
    img_b = mpimg.imread('Blindern.png')
    img_h,img_w,c = img_b.shape
    x,y = np.meshgrid(np.linspace(0,img_h,len_x),np.linspace(0,img_w,len_x))
    for j in range(Nt):
        fig = plt.figure()
        for i in range(len(plotnames)):
            ax = fig.add_subplot(2,2,i+1)
            imgplot = plt.imshow(img_b)
            #ax.title("%s" % classnames[i])
            img = "%s%04d.npy" % (plotnames[i],j)
            label_name = "%s = %s" % (para_name, parameter_values[i])
            #plt.plot(x_list[i],np.load(img),label=label_name)
            #ax.plot_wireframe(x_list[i],y_list[i],np.load(img), rstride=10, cstride=10,color=surf_color[i])
            #surf = ax.plot_surface(x_list[i],y_list[i],np.load(img), rstride=5, cstride=5,cmap=cm.coolwarm,linewidth=0, antialiased=False,vmin=0,vmax=max_val)
            CS = ax.contourf(y,x,np.load(img),50,cmap=cm.coolwarm,origin=origin,vmin=0,vmax=max_val,alpha=0.6) 
            ax.set_title(classnames[i])
            #ax.set_zlim(0,max_val)
            #ax.set_xlim3d(0,L)
            #ax.set_ylim3d(0,L)
            #ax.axes.xaxis.set_ticklabels([])
            #ax.axes.yaxis.set_ticklabels([])
            #ax.axes.zaxis.set_ticklabels([])
            #ax.set_xticks([])
        #cbar_ax = fig.add_axes([0.92, 0.15, 0.05, 0.7])
        #fig.colorbar(CS,cax=cbar_ax)
        #plt.plot([z_X,z_X],[-0.1,1.1],'k')
        #plt.text(z_X,-0.2,"x")
        #plt.axis([0,L,-0.1,1.1])
        #plt.legend(loc=3)
        #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
        #plt.suptitle(moviename)
        nt = (float(T)/Nt)*j
        #plt.title("time = %1.1f" % nt)
        fig.tight_layout()
        print j
        plt.savefig("movie_images/tmp_contourf%04d.png" % j)
        
        if(j%(sub_num-1) == 0 ):
            print j
            plt.savefig("plots/2D_gauss_wave%04d.png" % (j/(sub_num-1)))
        
        plt.close()

    os.system('doconce combine_images plots/2D_gauss_wave000* %s_contourf_sub.png' % moviename)
    os.system('rm plots/2D_gauss_wave000*')
    os.system('avconv -r 10 -i %s -vcodec libvpx %s_contourf.webm -y' %('movie_images/tmp_contourf%04d.png',moviename))
    for filename in glob.glob('movie_images/tmp_contourf*.png'):
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

def plot_volume(t,vol_list,moviename,classnames,T,title,t_size=1,x_size=1):
    #btt = 1.66116
    #x_size = 10*10
    for i in range(len(vol_list)):
        plt.plot(t/t_size,vol_list[i]/x_size,label=classnames[i])
    plt.axis([0,T,0,800])
    plt.xlabel('Days')
    plt.ylabel('Number')
    plt.title(title)
    #plt.legend(bbox_to_anchor=(0.,.9,1.0,.102), loc=3,ncol=4,mode="expand",borderaxespad=0.)
    plt.savefig('%s_number.png' % moviename)
    plt.show()
    
def print_phase(dt,t,phases,vol_list,classnames):
    for i in phases:
        cn = int(i/dt)
        print "time=%f" % t[cn]
        for j in range(len(vol_list)):
            vol = vol_list[j]
            print "%s = %3.2f" %(classnames[j],vol[cn])


def trav_wave(Nt,z,z_list,classnames,z_X,dim,moviename):
    if dim == '2D':
        z_X = np.sqrt(z_X**2+z_X**2) #Pythagoras
    I_area = np.zeros(Nt)
    I_area[:] = (z_list[1][:-1]+z_list[1][1:])/float(2) #Finds the height
    sum_area = I_area.sum()*(z[0]-z[1])
    print sum_area

    for i in range(len(z_list)):
        plt.plot(z,z_list[i],label= classnames[i])
    
    plt.xlabel("z")
    plt.axis([z_X-40,z_X,0,1])
    #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
    plt.title('Gaussian function from one side')
    plt.savefig("%s_trav_wave.png" % moviename)
    plt.show()
    plt.close()

def initial_susceptible_plot(plotname,moviename,para_name,L,T,z_X,max_val):
    x_list = []
    y_list = []
    surf_color = ['blue','green','red','cyan']
    
    img = "%s%04d.npy" % (plotname,0)
    print "img",img
    len_x = len(np.load(img))
    x,y = np.meshgrid(np.linspace(0,L,len_x),np.linspace(0,L,len_x))

    plotname = "%s*" %(plotname)
    Nt = len(glob.glob(plotname))
    print Nt
    sub_num = int((Nt-1)/3)
    
    fig = plt.figure()
    
    #img = "%s%04d.npy" % (plotname,0)
    #label_name = "%s = %s" % (para_name, parameter_values[i])
        #plt.plot(x_list[i],np.load(img),label=label_name)
    #ax.plot_wireframe(x,y,np.load(img), rstride=10, cstride=10,color=surf_color[0])
    CS = plt.contourf(x,y,np.load(img),50,cmap=cm.coolwarm,vmin=0,vmax=max_val,alpha=0.6) 
    plt.title("Initial values for susceptible")
    #plt.plot([z_X,z_X],[-0.1,1.1],'k')
    #plt.text(z_X,-0.2,"x")
    #plt.axis([0,L,-0.1,1.1])
    #ax.set_xlim3d(0,L)
    #ax.set_ylim3d(0,L)
    #ax.set_zlim3d(0,max_val*1.1)
    #plt.legend(loc=3)
    #plt.legend(bbox_to_anchor=(0.,1.02,1.,.102), loc=3,ncol=3,mode="expand",borderaxespad=0.)
    #plt.suptitle(moviename)
    cbar_ax = fig.add_axes([0.90, 0.15, 0.05, 0.7])
    fig.colorbar(CS,cax=cbar_ax)
    plt.savefig(moviename)
        
