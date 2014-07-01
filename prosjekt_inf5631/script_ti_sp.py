import os
from build_plot import *
from wave_front import wave_front
from scaling import *

#Print several versions of time derivate solution
"""
r_list = [0.5,1]
plotnames = []
eq_list = ["time"]
for i in eq_list:
	for j in r_list:
		plotname = ("plot_data/%s_r_%2.3f" % (i,j)).replace(".","_")
		plotnames.append(plotname)
		os_name = "python time_derivate.py 1 %2.3f %s" % (j,plotname)
		print os_name
		os.system(os_name)
"""
#Print several versions of time derivate solution
"""
k_list = [0.01]#,0.1,1]#,1]#,0.5,1,5]
eq_list = ["constant"]#,"abs_std","ordinary"]
for i in k_list:
	for j in eq_list:
		filename = ("movies/spatial_%s_m_%1.2f" % (j,i)).replace(".","_")
		os_name = "python spatial_diff_general.py --k %1.2f --method %s --m_n %s.webm" % (i,j,filename)
		print os_name
		os.system(os_name)
"""
"""
m_list = [0.1,2,8]#,2,3,4]#,0.5,1,5]
eq_list = ["abs_std"]#,"ordinary"]
for i in m_list:
	for j in eq_list:
		filename = ("movies/spatial_%s_m_%1.1f" % (j,i)).replace(".","_")
		os_name = "python spatial_diff_general.py --m %1.2f --method %s --m_n %s.webm" % (i,j,filename)
		print os_name
		os.system(os_name)
"""

Nx_list = [100,100,100]#,100,100]
N_list = [100,500,2000]
L = 20
T = 10
fg_list = [1,5,20]	#frame gap


#para_list = [1] #parameter list
eq_list = ["constant"]
plotnames = []

for i in range(len(Nx_list)):
	for j in eq_list:
		plotname = ("plot_data/%s_M_%2.3f" % (j,i)).replace(".","_")
		plotnames.append(plotname)
		os_name = "python reac_diff_eq.py --method %s --p_n %s --r 1 --M 1 --k 1 --picard True --Nx %i --N %i --L %i --T %i --fg %i" % (j,plotname,Nx_list[i],N_list[i],L,T,fg_list[i])
		print os_name
		#os.system(os_name)


plotname = "plot_data/wave_front"
plotnames.append(plotname)
wave_front(plotname,Nx_list[0],N_list[0]/fg_list[0],L,T)
N_list.append("analytical")
"""
m_list = [0.5,1,2]
for i in m_list:
        plotname = ("plot_data/scaling_%2.3f" % i)
        plotnames.append(plotname)
        scaling(plotname,Nx_list[0],N_list[0]/fg_list[0],L,T,i)
"""
build_plot(plotnames,"movies/stability_analysis",N_list,"N",L,T)
#build_subplot(plotnames,"submovies/ordinary_sub",para_list,"k")
"""
error_list = check_error(plotnames[-1],plotnames,L)
for i in range(len(plotnames)-1):
	if (i>0):
		power = np.log(error_list[i-1]/error_list[i])/np.log(N_list[i]/N_list[i-1])
	else:
		power = 0
	print("N = %s, err = %f pow = %f" % (N_list[i],error_list[i],power))
"""
os.system('rm plot_data/*')
