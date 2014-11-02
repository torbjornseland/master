import matplotlib.image as mpimg
import numpy as np

def gamma_mapping(gamma_list):
    img = mpimg.imread("Blindern.png")
    img_h,img_w,c = img.shape
    free_area = img[img_h-1][img_w-1][0] #White Blindern	

    
    w,h = gamma_list[0].shape
    h_re = float(img_h)/h
    w_re = float(img_w)/w
    for i in range(w):
        for j in range(h):
            if (img[int(j*h_re)][int(i*w_re)][0] == free_area): 
                for gamma in gamma_list[1:]:
                    gamma[i,j] = 0


    
    return gamma_list

"""
a_list = np.ones([10,10])
print a_list

gamma_mapping([a_list])

print a_list
"""
