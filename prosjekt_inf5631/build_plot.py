import matplotlib.pyplot as plt
import numpy as np
import os,glob

Nx = 200
L = 10
x = np.linspace(0,L,Nx+1)


def build_plot(plotnames,moviename,parameter_values,para_name):
	plotname = "%s*" %(plotnames[0])
	Nt = len(glob.glob(plotname))
	print Nt
	for j in range(Nt):
		for i in range(len(plotnames)):
			img = "%s%04d.npy" % (plotnames[i],j)
			label_name = "%s = %s" % (para_name, parameter_values[i])
			plt.plot(x,np.load(img),label=label_name)
		plt.axis([0,L,-1,1.2])
		plt.legend()
		plt.suptitle(moviename)
		plt.title("Change in the reproduction rate")
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

