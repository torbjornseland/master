import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as anm
import scitools.std as sci
import numpy as np
import random
import time
from math import sqrt
import os, sys,glob



img = mpimg.imread(sys.argv[4])
img_h,img_w,c = img.shape

min_size = min(img_h,img_w)
free_area = img[img_h-1][img_w-1][0] #White Blindern	


class zombie(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.s = 0.1
		self.getcolor = 'r'

	def update(self, everyone):
		c = 1
		dx = 0
		dy = 0
		r_min = min_size
		if(self.getcolor == 'r'):
			for e in everyone:			#Run through all objects
				if e.color() == "b":	#Checking if the object is blue
					mx, my = e.coordinates()	#Returing the coordinate for the element
					r = sqrt((self.x -mx)**2 + (self.y -my)**2)

					if (r < r_min and img[my][mx][0] != free_area): 
						r_min = r
						mx_min = mx
						my_min = my

			if r_min < min_size:
				c += 1
				dx += mx_min - self.x
				dy += my_min - self.y
					
			dx /= c
			dy /= c
			
			if(img[self.y + self.s*dy][self.x + self.s*dx][0] == free_area):	
				self.x = self.x 
				self.y = self.y 
			else:
				self.x = self.x + self.s*dx
				self.y = self.y + self.s*dy
			


	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor

class man(object):
	def __init__(self,x,y,col):
		self.x = x
		self.y = y
		self.s = 1 # Speed
		self.getcolor = col
		self.dead = 0
		

	def update (self, everyone):

		c = 1
		dx = 0
		dy = 0
		for e in everyone:
			if e.color() == "r":	#Checking if the object is a zombie
				mx, my = e.coordinates()
				r = sqrt((self.x - mx)**2 + (self.y - my)**2)
				if r < min_size*0.1:
					c += 1
					dx += mx - self.x
					dy += my - self.y
				if r < min_size*0.05:	# if it is closer than 0.01 the human will stop moving
					self.s = 0
				
				if r < min_size*0.01: 
					self.getcolor = 'w'
		
		dx /= c
		dy /= c
		
		
		
		
		check_x = self.x - self.s*dx #Checking if x is inside the map
		
		if(check_x > 0 and check_x < img_w):
			self.x = check_x
		else:
			self.x = self.x + self.s*dx
		
		check_y = self.y - self.s*dy #Checking if y is inside the map
		if(check_y > 0 and check_y < img_h):
			self.y = check_y
		else:
			self.y = self.y + self.s*dy

		if(self.getcolor == 'w'):
			self.dead += 1

	def coordinates(self):
		return (self.x,self.y)

	def color(self):
		return self.getcolor

	def deadTime(self):
		return self.dead
	
	def getfight(self):
		return self.fight

def one_step(everyone):
	counter = 0
	x = np.zeros(len(everyone))
	y = np.zeros(len(everyone))
	c = [0]*len(everyone)
	for e in everyone:
		e.update(everyone)
		p = e.coordinates()
		x[counter] = p[0]
		y[counter] = p[1]
		c[counter] = e.color()
		
		if(e.color() == 'w' and e.deadTime() > 30):
			everyone[counter] = zombie(p[0],p[1])
		counter += 1
	
	return x,y,c

def first_step(everyone):
	for e in everyone:
		p = e.coordinates()
		x.append(p[0])
		y.append(p[1])
		c.append(e.color())
	
	return x,y,c




ZN = int(sys.argv[1])
zombies = []
for i in range(0,ZN):		#Making zombies
	x, y = random.uniform(0,img_w), random.uniform(0,img_h)
	while(img[y][x][0] == free_area):
		x, y = random.uniform(0,img_w), random.uniform(0,img_h)
			
	z = zombie(x,y)
	zombies.append(z)

MN = int(sys.argv[2])
men = []
first = True
for i in range(0,MN):
	x, y = random.uniform(0,img_w), random.uniform(0,img_h)

	m = man(x,y,'b')
	men.append(m)


everyone = zombies + men
x = []
y = []
c = []



files = []


counter = 0
steps = int(sys.argv[3])
for i in range(0,steps):
	
	imgplot = plt.imshow(img)
	if(counter == 0):
		x, y, c = first_step(everyone)
	else:
		x, y, c = one_step(everyone)
	plt.scatter(x,y, c=c)
	plt.savefig('moviefiles/tmp%04d.png'% counter)
	plt.close()
	
	for e in everyone:
		e.update(everyone)
	counter += 1


savefile = sys.argv[5]
sci.movie('moviefiles/tmp*.png',output_file= savefile, fps=6)
for filename in glob.glob('moviefiles/tmp*.png'):
	os.remove(filename)
os.system("animate "+savefile)

"""
fps = 10
sci.movie('moviefiles/tmp*.png', encoder='html', fps=fps, output_file='movie.html')


codec2ext = dict(flv='flv', libx64='mp4', libvpx='webm',libtheora='ogg')
filespec = 'moviefiles/tmp%04d.png'
movie_program = 'avconv'
for codec in codec2ext:
	ext = codec2ext[codec]
	cmd = '%(movie_program)s -r %(fps)d -i %(filespec)s -vcodec %(codec)s movie.%(ext)s' % vars()
        os.system(cmd)
	

"""

