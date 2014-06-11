import os
from build_plot import *

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
para_list = [0] #parameter list
eq_list = ["constant"]
plotnames = []
for i in para_list:
	for j in eq_list:
		plotname = ("plot_data/%s_M_%2.3f" % (j,i)).replace(".","_")
		plotnames.append(plotname)
		os_name = "python reac_diff_eq.py --method %s --p_n %s --r 1 --M 1 --k %g --picard True " % (j,plotname,i)
		print os_name
		os.system(os_name)
build_plot(plotnames,"paramovies/%s_fisher_few_points" % eq_list[0],para_list,"k")
#build_subplot(plotnames,"submovies/ordinary_sub",para_list,"k")
os.system('rm plot_data/*')
