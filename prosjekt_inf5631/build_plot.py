import matplotlib.pyplot as plt
import numpy as np
import os,glob

#Nx = 2000
#L = 60
#x = np.linspace(-L,L,Nx+1)


def build_plot(plotnames,moviename,parameter_values,para_name,L,T):
	x_list = []
	for i in plotnames:
		img = "%s%04d.npy" % (i,0)
		len_x = len(np.load(img))
		x = np.linspace(0,L,len_x)
		x_list.append(x)
	plotname = "%s*" %(plotnames[0])
	Nt = len(glob.glob(plotname))
	print Nt
	for j in range(Nt):
		for i in range(len(plotnames)):
			img = "%s%04d.npy" % (plotnames[i],j)
			if not(parameter_values[i]=="analytical"):
				label_name = "%s = %2.3f" % (para_name, float(parameter_values[i]))
			else:
				label_name = "%s = %s" % (para_name, parameter_values[i])
			plt.plot(x_list[i],np.load(img),label=label_name)
		plt.axis([0,L,-0.2,1.2])
		plt.legend(loc=3)
		plt.suptitle(moviename)
		plt.title("Change in the carrying capacity")
		plt.savefig("tmp%04d.png" % j)
		plt.close()

	os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
	for filename in glob.glob('tmp*.png'):
		os.remove(filename)

def build_subplot(plotnames,moviename,parameter_values,para_name):
	plotname = "%s*" %(plotnames[0])
	Nt = len(glob.glob(plotname))
	print Nt
	for j in range(Nt):
		for i in range(len(plotnames)):
			img = "%s%04d.npy" % (plotnames[i],j)
			plt.subplot(2,2,i+1)
			plt.plot(x,np.load(img))
			plt.axis([0,L,-1,1])
			title_name = "%s = %s" % (para_name, parameter_values[i])
			plt.title(title_name)
		#plt.legend(parameter_values)
		plt.suptitle("Change in the tolerance")
		plt.savefig("tmp%04d.png" % j)
		plt.close()
	os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm' %('tmp%04d.png',moviename))
	for filename in glob.glob('tmp*.png'):
		os.remove(filename)


def check_error(analytical_sol,plotnames,L):
	x_list = []
	for i in plotnames:
		img = "%s%04d.npy" % (i,0)
		len_x = len(np.load(img))
		x = np.linspace(-L,L,len_x)
		x_list.append(x)
	plotname = "%s*" %(plotnames[0])
	Nt = len(glob.glob(plotname))
	print Nt
	error_list = [0]*len(plotnames)
	for j in range(Nt):
		analytical = np.load("%s%04d.npy" % (analytical_sol,j))
		for i in range(len(plotnames)):
			img = "%s%04d.npy" % (plotnames[i],j)
			ch_err = np.max(abs(analytical-np.load(img)))
			if(ch_err > error_list[i]):
				error_list[i] = ch_err
	return error_list
