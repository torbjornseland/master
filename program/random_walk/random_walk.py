import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as anm
import scitools.std as sci
import numpy as np
import random
import time
from math import sqrt,pi,cos,sin
import os, sys,glob

import random as rd
import numpy as np



def define_command_line_options():
		import argparse
		parser = argparse.ArgumentParser()
		parser.add_argument('--ZN', '--zombie_number', type=int,
					default=3, help='Number of zombies at initial time',
					metavar='ZN')
		parser.add_argument('--HN', '--human_number', type=int,
					default=50, help='Number of humans at initial time',
					metavar='HN')
		parser.add_argument('--S', '--time_steps', type=int,
					default=40, help='Numbers of time steps',
					metavar='steps')
		parser.add_argument('--area', '--area_map', type=str,
					default='Blindern.png', help='Map of the area',
					metavar='area_map')
		parser.add_argument('--g', '--grid_size', type=int,
					default=10, help='Numbers of points in each direction',
					metavar='grid_size')
		parser.add_argument('--ZK', '--zombie_kill', type=float,
					default=0.5, help='Percent chance for a zombie to be killed',
					metavar='zombie_kill')
		parser.add_argument('--HI', '--human_infection', type=float,
					default=0.5, help='Percent chance for a human to be infected',
					metavar='human_infected')
		parser.add_argument('--ZA', '--zombie_awake', type=float,
					default=0.0, help='Percent chance for a zombie to wake up from dead',
					metavar='zombie_awake')
		parser.add_argument('--IZ', '--infected_zombie', type=float,
					default=0.2, help='Percent chance for an infected human to be zombie',
					metavar='infected_zombie')
		parser.add_argument('--ID', '--infected_dead', type=float,
					default=0.1, help='Percent chance for an infected human to die',
					metavar='infected_dead')
		parser.add_argument('--makeplot', action='store_true',
					help='display simulations of the zombies and humans')
		parser.add_argument('--makegraph', action='store_true',
					help='display the change in zombies and humans during the time')
		parser.add_argument('--savefile',  type=str,
					default='movie.gif', help='Name and path to the movie',
					metavar='savefile')
		
		return parser

def read_command_line():
    parser = define_command_line_options()
    args = parser.parse_args()
    print 'ZN={}, HN={}, Steps={}, area={}, grid_size={}, \nzombie_kill={}, human_infected={}, zombie_awake={}, \ninfected_zombie={}, infected_dead={}, makeplot={}, \nmakegraph={}, savefile={}'.format(
        args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile )
    return args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile


class zombie(object):
	def __init__(self,x,y,my_id):
		self.x = x
		self.y = y
		self.s = 0.1
		self.getcolor = 'r'
		self.my_id = my_id

	def update(self, everyone):
		c = 1
		dx = 0
		dy = 0
		
		i = int(self.x*grid_size/img_w)
		j = int(self.y*grid_size/img_h)
		
		Zombie_force = [] 
		Human_force = [] 
		
		#print "HMO",HMO[i:i+3,j:j+3]
		for k in range(3):
			for l in range(3):
				Zombie_force.extend(ZMO[i+k,j+l])
				Human_force.extend(HMO[i+k,j+l])
				del HMO[i+k,j+l][:] #Only allowed to do one battle each round
		
		#print "HMO after",HMO[i:i+3,j:j+3]
		#Fighting
		z_power = len(Zombie_force)
		h_power = len(Human_force)
				
		
		if(h_power != 0):
			for k in range(h_power):
				human_infec = rd.random()
				zombie_surv = rd.random()
			
				if(zombie_surv < (ZK+0.0*h_power)):
					self.getcolor = 'm' 	#Zombie is dying
					break
				if(human_infec < (HI+0.0*z_power)):
					everyone[Human_force[k]].getcolor = 'c'	#Human getting infected

				
				
			
										

		
		#Random walk
		direction = rd.uniform(0,2*pi)	
		
		test_x = self.x + step_x*cos(direction) 
		test_y = self.y + step_y*sin(direction) 
	
	
		if(self.getcolor == 'r'):
				#Removing zombie from position	
				count_pos = 0 	
				for k in ZMO[i+1,j+1]:
					if(k == self.my_id):
						del ZMO[i+1,j+1][count_pos]
					count_pos += 1

				if(test_x < img_w and test_x > 0):
					self.x = test_x
					
				if(test_y < img_h and test_y > 0):
					self.y = test_y	
				
				#Giving the zombie a new position
				i = (self.x//step_x)
				j = (self.y//step_y)
				ZMO[i+1,j+1].append(self.my_id)
		
			
	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor

	def get_id(self):
		return self.my_id

class man(object):
	def __init__(self,x,y,col,my_id):
		self.x = x
		self.y = y
		self.s = 1 # Speed
		self.getcolor = col
		self.dead = 0
		self.my_id = my_id
		

	def update (self, everyone):

		c = 1
		dx = 0
		dy = 0

		
		i = int(self.x*grid_size/img_w)
		j = int(self.y*grid_size/img_h)
		

		direction = rd.uniform(0,2*pi)	
		
		test_x = self.x + step_x*cos(direction) 
		test_y = self.y + step_y*sin(direction) 
		
			
		#Removing human from position
		count_pos = 0 	
		for k in HMO[i+1,j+1]:
			if(k == self.my_id):
				del HMO[i+1,j+1][count_pos]
			count_pos += 1


		if(test_x < img_w and test_x > 0):
			self.x = test_x
			
		if(test_y < img_h and test_y > 0):
			self.y = test_y	
		
		#Giving the human/infected a new position
		i = (self.x//step_x)
		j = (self.y//step_y)
		HMO[i+1,j+1].append(self.my_id)
	
		
	def coordinates(self):
		return (self.x,self.y)

	def color(self):
		return self.getcolor

	def deadTime(self):
		return self.dead
	
	def getfight(self):
		return self.fight

	def get_id(self):
		return self.my_id

class dead(object):
	def __init__(self,x,y,my_id):
		self.x = x
		self.y = y
		self.s = 0.1
		self.getcolor = 'k'
		self.my_id = my_id

	def update(self, everyone):
		c = 1

	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor
	
	def get_id(self):
		return self.my_id

class infected(object):
	def __init__(self,x,y,my_id):
		self.x = x
		self.y = y
		self.s = 0.1
		self.getcolor = 'w'
		self.my_id = my_id

	def update(self, everyone):
		c = 1

		direction = rd.uniform(0,2*pi)	
		
		test_x = self.x + step_x*cos(direction) 
		test_y = self.y + step_y*sin(direction) 
		
		if(test_x < img_w and test_x > 0):
			self.x = test_x
		if(test_y < img_h and test_y > 0):
			self.y = test_y			

	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor
	
	def get_id(self):
		return self.my_id
	
	
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
		

		#infected
		if(e.color() == 'w'):
			inf_rand = rd.random()
			if (inf_rand < IZ): #percent chance of beeing a Zombie
				everyone[counter] = zombie(p[0],p[1],e.get_id())
			elif(inf_rand < (IZ+ID)):#percent change of dying 
				everyone[counter] = dead(p[0],p[1],e.get_id())
			else:
				pass
	
		#dead	
		if(e.color() == 'k'):
			dead_rand = rd.random()
			if (dead_rand < ZA): #percent chance of beeing a Zombie
				everyone[counter] = zombie(p[0],p[1],e.get_id())
			else:
				pass
		
		
			
				
		if(e.color() == 'c'):	#getting infected
			everyone[counter] = infected(p[0],p[1],e.get_id())
		if(e.color() == 'm'):	#dying to dead
			everyone[counter] = dead(p[0],p[1],e.get_id())
			
		counter += 1
	
	return x,y,c

def first_step(everyone):
	for e in everyone:
		p = e.coordinates()
		x.append(p[0])
		y.append(p[1])
		c.append(e.color())
	
	return x,y,c



#############################--Script--#####################################


ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile = read_command_line()


img = mpimg.imread(area_map)
img_h,img_w,c = img.shape

step_x = (img_w/float(grid_size))
step_y = (img_h/float(grid_size))

ZMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
for i in range(grid_size+2):
	for j in range(grid_size+2):
		ZMO[i,j] = [] 



Human_matrix = np.zeros([grid_size+2,grid_size+2])
HMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Human matrix old
for i in range(grid_size+2):
	for j in range(grid_size+2):
		HMO[i,j] = [] 


zombies = []
for i in range(0,ZN):		#Making zombies
	x_start = rd.randint(0,grid_size-1)
	y_start = rd.randint(0,grid_size-1)
	
	x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
	z = zombie(x,y,i)
	zombies.append(z)
	ZMO[x_start+1,y_start+1].append(i)	#Zombie matrix old



men = []
first = True
for i in range(0,HN):
	x_start = rd.randint(0,grid_size-1)
	y_start = rd.randint(0,grid_size-1)	

	x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
	m = man(x,y,'b',i+ZN)
	men.append(m)

	HMO[x_start+1, y_start+1].append(i+ZN) #Human matrix old


everyone = zombies + men
x = []
y = []
c = []



files = []


counter = 0


steps_array = np.linspace(0,steps,steps+1) 
zombie_array = np.zeros(steps+1)
human_array = np.zeros(steps+1)
infected_array = np.zeros(steps+1)
dead_array = np.zeros(steps+1)

zombie_array[0] = len(zombies)
human_array[0] = len(men)


for i in range(0,steps):
	
	
	if(counter == 0):
		x, y, c = first_step(everyone)
	else:	
		x, y, c = one_step(everyone)	
	
	if makeplot:
		fig = plt.figure()
		imgplot = plt.imshow(img)
		#ax = fig.gca()
		#ax.set_xticks(np.linspace(0,img_w,grid_size+1))
		#ax.set_yticks(np.linspace(0,img_h,grid_size+1))
		plt.scatter(x,y, c=c)
		#plt.grid()
		plt.savefig('moviefiles/tmp%04d.png'% counter)
		plt.close()

	
	
	if makegraph:
		for e in everyone:
			if (e.color() == 'r'):
				zombie_array[i+1] = zombie_array[i+1]+ 1
			elif (e.color() == 'b'):
				human_array[i+1] = human_array[i+1]+ 1
			elif (e.color() == 'w' or e.color() == 'c'):
				infected_array[i+1] = infected_array[i+1]+ 1
			else:
				dead_array[i+1] = dead_array[i+1] + 1


	counter += 1


	

if makeplot:
	
	sci.movie('moviefiles/tmp*.png',output_file= savefile, fps=6)
	for filename in glob.glob('moviefiles/tmp*.png'):
		os.remove(filename)
	os.system("animate "+savefile)
	"""
	#fps = 10
	#sci.movie('moviefiles/tmp*.png', encoder='html', fps=fps, output_file='movie.html')


	#codec2ext = dict(flv='flv', libx64='mp4', libvpx='webm',libtheora='ogg')
	codec2ext = dict(libvpx='webm')
	filespec = 'moviefiles/tmp%04d.png'
	movie_program = 'avconv'
	for codec in codec2ext:
		ext = codec2ext[codec]
		cmd = '%(movie_program)s -r %(fps)d -i %(filespec)s -vcodec %(codec)s movie.%(ext)s' % vars()
	os.system(cmd)
	

	for filename in glob.glob('moviefiles/tmp*.png'):
		os.remove(filename)
	"""


if makegraph:
	plt.plot(steps_array, zombie_array,'r',label='Zombies')
	plt.plot(steps_array, human_array,'b', label='Humans')
	plt.plot(steps_array, infected_array,'w', label='Infected')
	plt.plot(steps_array, dead_array,'k', label='Dead')
	plt.legend()

	plt.axis([0,steps,0,len(everyone)])
	plt.show()
	

