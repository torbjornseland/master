
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import matplotlib.animation as anm
import scitools.std as sci
import numpy as np
import random
import time
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np

import pygame
from pygame.sprite import Sprite





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
		parser.add_argument('--mode',  type=str,
					default='moving_smart', help='How they move and interact',
					metavar='mode')
		
		return parser

def read_command_line():
	parser = define_command_line_options()
	args = parser.parse_args()
	print 'ZN={}, HN={}, Steps={}, area={}, grid_size={},\nzombie_kill={}, human_infected={}, zombie_awake={},\ninfected_zombie={}, infected_dead={}, makeplot={},\nmakegraph={}, savefile={}, mode={}'.format(
		args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile, args.mode )
	return args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile, args.mode

class creature(object):
	def __init__(self,x,y,my_id,screen,getcolor,img_creature):
		self.x = x
		self.y = y
		self.my_id = my_id
		self.screen = screen
		self.no_steps = 0
		self.getcolor = getcolor
		self.direction = 0

		self.base_image = pygame.image.load(img_creature).convert_alpha()
		self.image = self.base_image
		self.image_w, self.image_h = self.image.get_size()


	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor

	def get_id(self):
		return self.my_id
	
	def blitme(self):
		#self.direction = 0
		#print "dir", self.direction
		self.image = pygame.transform.rotate(
			self.base_image, (-self.direction*(360/(2*pi))-90))
		draw_pos = self.image.get_rect().move(
			self.x - self.image_w / 2, 
			self.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

	def get_screen(self):
		return self.screen



class zombie(creature):
	def __init__(self,*args):
		super(zombie,self).__init__(*args)
		
		self.dx = 0
		self.dy = 0

	def update(self, everyone):
		r_min = min_size
		mx_min = 0
		my_min = 0
		mx_way = 1
		my_way = 1
		
		test_x = self.x
		test_y = self.y
		
		i = int(self.x*grid_size/img_w)
		j = int(self.y*grid_size/img_h)
		
		if(i == grid_size):
			print "inne her"
			i = 0
		if(j == grid_size):
			print "inne j"
			j = 0
		
		Zombie_force = [] 
		Human_force = [] 

		for k in range(3):
			for l in range(3):
				Zombie_force.extend(ZMO[i+k,j+l])
				Human_force.extend(HMO[i+k,j+l])
				del HMO[i+k,j+l][:] #Only allowed to do one battle each round

		#Fighting
		z_power = len(Zombie_force)
		h_power = len(Human_force)
	   
		if(h_power != 0):
			for k in range(h_power):
				human_infec = rd.random()
				zombie_surv = rd.random()
				if(human_infec < (HI+0.0*z_power)):
					everyone[Human_force[k]].getcolor = 'c' #Human getting infected
				if(zombie_surv < (ZK+0.0*h_power)):
					self.getcolor = 'm'		#Zombie is dying
					break

										

		if(self.getcolor == 'r'): 
			#Checking the mode
			if(mode == 'hunting' or mode == 'moving_smart'):
				for e in everyone:			#Run through all objects
					if e.color() == "b":	#Checking if the object is blue
						mx, my = e.coordinates()	#Returing the coordinate for the element
						
						if(abs(self.x-mx) <= img_w/2.):
							x_way = -1
							x_dir = self.x-mx
						else:
							x_way = 1
							if((self.x-mx)<0):
								x_dir = -1*(img_w-abs(self.x-mx))
							else:
								x_dir = img_w-abs(self.x-mx)
						
						if(abs(self.y-my) <= img_h/2.):
							y_way = -1
							y_dir = self.y-my
						else:
							if((self.y-my)<0):
								y_dir = -1*(img_h-abs(self.y-my))
							else:
								y_dir = (img_h-abs(self.y-my))
							y_way = 1

					
						#print "x_dir",x_dir
						r = sqrt((x_dir)**2 + (y_dir)**2)

						if (r < r_min): # and img[my][mx][0] != free_area):

							r_min = r
							mx_min = x_dir
							my_min = y_dir
							mx_way = x_way
							my_way = y_way
							
				if (r_min < min_size and r_min!= 0):
					self.dx = (mx_min)/float(r_min)*mx_way
					self.dy = (my_min)/float(r_min)*my_way
					
					test_x = self.x + step_x*self.dx
					test_y = self.y + step_y*self.dy
					self.direction = atan2((step_y*self.dy),(step_x*self.dx))
				else:
					self.dx = 0
					self.dy = 0
				

				
			if(mode == 'random' or (mode == 'moving_smart' and r_min == min_size)):
				if (self.no_steps == 0):
					self.direction = rd.uniform(0,2*pi)
					self.no_steps = rd.randint(1,20)
		
				test_x = self.x + step_x*cos(self.direction) 
				test_y = self.y + step_y*sin(self.direction)
				self.no_steps -= 1
		 
	
	
			#Removing zombie from position	
			count_pos = 0
			for k in ZMO[i+1,j+1]:
				if(k == self.my_id):
					del ZMO[i+1,j+1][count_pos]
				count_pos += 1

			if(test_x > img_w):
				self.x = test_x -img_w
			elif(test_x < 0):
				self.x = img_w + test_x
			else:
				self.x = test_x
			
			if(test_y > img_h):
				self.y = test_y -img_h
			elif(test_y < 0):
				self.y = img_h + test_y
			else:
				self.y = test_y
				
			#Giving the zombie a new position
			i = int(self.x*grid_size/img_w)
			j = int(self.y*grid_size/img_h)
			ZMO[i+1,j+1].append(self.my_id)
			#print "each round ZMN", ZMN	
			
	def coordinates(self):
		return super(zombie,self).coordinates()

	def color(self):
		return super(zombie,self).color()

	def get_id(self):
		return super(zombie,self).get_id()
	
	def blitme(self):
		#self.direction = 0
		#print "dir", self.direction
		self.image = pygame.transform.rotate(
			self.base_image, (-self.direction*(360/(2*pi))-90))
		draw_pos = self.image.get_rect().move(
			self.x - self.image_w / 2, 
			self.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

	def get_screen(self):
		return super(zombie,self).get_screen()

class man(creature):
	def __init__(self,*args):
		super(man,self).__init__(*args)

	def update (self, everyone):

		c = 1
		dx = 0
		dy = 0
		hyp = 0
		test_x = self.x
		test_y = self.y
		
		i = int(self.x*grid_size/img_w)
		j = int(self.y*grid_size/img_h)
		
		if(mode == 'moving_smart' or mode == 'hunting'):
			for e in everyone:
				if e.color() == "r":	#Checking if the object is a zombie
					mx, my = e.coordinates()

					if(abs(self.x-mx) <= img_w/2.):
						x_way = -1
						x_dir = self.x-mx
					else:
						if((self.x-mx)<0):
							x_dir = -1*(img_w-abs(self.x-mx))
						else:
							x_dir = img_w-abs(self.x-mx)
						x_way = 1
						
					if(abs(self.y-my) <= img_h/2.):
						y_way = -1
						y_dir = self.y-my
					else:
						if((self.y-my)<0):
							y_dir = -1*(img_h-abs(self.y-my))
						else:
							y_dir = (img_h-abs(self.y-my))
						y_way = 1

					
					r = sqrt((x_dir)**2 + (y_dir)**2)
					
					if r < (min_size*0.5):
						dx += (min_size*0.5-r)*x_dir
						dy += (min_size*0.5-r)*y_dir
						mx_way = x_way
						my_way = y_way
						"""
						print "dx",dx
						print "dy",dy
						print "x_dir",x_dir
						print "y_dir", y_dir
						"""
			
			hyp = sqrt(dx**2 + dy**2)	
		
			if(hyp != 0):
				dx = dx/float(hyp)*mx_way
				dy = dy/float(hyp)*my_way
			if((dx != 0 or dy != 0) or mode=='hunting'):
				test_x = self.x - step_x*dx #Checking if x is inside the map	
				test_y = self.y - step_y*dy #Checking if y is inside the map
				
				self.direction = atan2((step_y*dy),(step_x*dx))+pi
		if(mode == 'random' or (mode=='moving_smart' and hyp == 0)) :
			if (self.no_steps == 0):
				self.direction = rd.uniform(0,2*pi)
				self.no_steps = rd.randint(1,20) 
		
			test_x = self.x + step_x*cos(self.direction) 
			test_y = self.y + step_y*sin(self.direction)
			self.no_steps -= 1	
				
			
		#Removing human from position
		count_pos = 0	
		for k in HMO[i+1,j+1]:
			if(k == self.my_id):
				del HMO[i+1,j+1][count_pos]
			count_pos += 1

		#Sending them through the wall
		if(test_x > img_w):
			self.x = test_x -img_w
		elif(test_x < 0):
			self.x = img_w + test_x
		else:
			self.x = test_x
			
		if(test_y > img_h):
			self.y = test_y -img_h
		elif(test_y < 0):
			self.y = img_h + test_y
		else:
			self.y = test_y
		
		
		#Giving the human/infected a new position
		i = (self.x//grid_x)
		j = (self.y//grid_y)
		HMO[i+1,j+1].append(self.my_id)
	
		
	def coordinates(self):
		return (self.x,self.y)

	def color(self):
		return self.getcolor

	def get_id(self):
		return self.my_id

	def blitme(self):
		
		self.image = pygame.transform.rotate(
			self.base_image, (-self.direction*(360/(2*pi))-90))
		
		draw_pos = self.image.get_rect().move(
			self.x - self.image_w / 2, 
			self.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

class dead(creature):
	def __init__(self,*args):
		super(dead,self).__init__(*args)
	
	def update(self, everyone):
		c = 1

	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return self.getcolor
	
	def get_id(self):
		return self.my_id
	
	def blitme(self):
		draw_pos = self.image.get_rect().move(
			self.x - self.image_w / 2, 
			self.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)

class infected(creature):
	def __init__(self,*args):
		super(infected,self).__init__(*args)

	def update(self, everyone):
		c = 1

		if (self.no_steps == 0):
			self.direction = rd.uniform(0,2*pi)
			self.no_steps = rd.randint(1,20) 
		
		test_x = self.x + step_x*cos(self.direction) 
		test_y = self.y + step_y*sin(self.direction)
		self.no_steps -= 1	
		
		if(test_x > img_w):
			self.x = test_x -img_w
		elif(test_x < 0):
			self.x = img_w + test_x
		else:
			self.x = test_x
			
		if(test_y > img_h):
			self.y = test_y -img_h
		elif(test_y < 0):
			self.y = img_h + test_y
		else:
			self.y = test_y

	def coordinates(self):
		return super(infected,self).coordinates()

	def color(self):
		return super(infected,self).color()

	def get_id(self):
		return super(infected,self).get_id()
	
	def blitme(self):
		self.image = pygame.transform.rotate(
			self.base_image, (-self.direction*(360/(2*pi))-90))
		
		draw_pos = self.image.get_rect().move(
			self.x - self.image_w / 2, 
			self.y - self.image_h / 2)
		self.screen.blit(self.image, draw_pos)
	
	
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
				everyone[counter] = zombie(p[0],p[1],e.get_id(),screen,'r','pictures/zombie.png')
			elif(inf_rand < (IZ+ID)):#percent change of dying 
				everyone[counter] = dead(p[0],p[1],e.get_id(),screen,'k','pictures/tombstone.png')
			else:
				pass
	
		#dead		
		if(e.color() == 'k'):
			dead_rand = rd.random()
			if (dead_rand < ZA): #percent chance of beeing a Zombie
				everyone[counter] = zombie(p[0],p[1],e.get_id(),screen,'r','pictures/zombie.png')
			else:
				pass
		
		if(e.color() == 'c'):	#getting infected
			everyone[counter] = infected(p[0],p[1],e.get_id(),screen,'w','pictures/infected.png')
		if(e.color() == 'm'):	#dying to dead
			everyone[counter] = dead(p[0],p[1],e.get_id(),screen,'k','pictures/tombstone.png')
	

		
		e.blitme()	
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


ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile, mode = read_command_line()
game_on = True


	


pygame.init()		

background = pygame.image.load('pictures/Blindern2.jpg')


#background.convert()
background_size = background.get_size()
background_rect = background.get_rect()
screen = pygame.display.set_mode(background_size)


background = background.convert()
clock = pygame.time.Clock()





img = mpimg.imread('pictures/Blindern2.jpg')
img_h,img_w,c = img.shape
min_size = min(img_h,img_w)*0.3

grid_x = (img_w/float(grid_size))
grid_y = (img_h/float(grid_size))

step_x = grid_x*0.2
step_y = grid_y*0.2

ZMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
ZMN = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
M_emp = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
for i in range(grid_size+2):
	for j in range(grid_size+2):
		ZMO[i,j] = [] 
		ZMN[i,j] = [] 
		M_emp[i,j] = [] 



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
	
	z = zombie(x,y,i,screen,'r','pictures/zombie.png')
	zombies.append(z)
	ZMO[x_start+1,y_start+1].append(i)	#Zombie matrix old



men = []
first = True
for i in range(0,HN):
	x_start = rd.randint(0,grid_size-1)
	y_start = rd.randint(0,grid_size-1)

	x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
	m = man(x,y,i+ZN,screen,'b','pictures/redhead.png')
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

if not game_on: 
		for i in range(0,steps):
		
			if(counter == 0):
				x, y, c = first_step(everyone)
			else:
				x, y, c = one_step(everyone)	
			
			if makeplot:
				fig = plt.figure()
				imgplot = plt.imshow(img)
				plt.scatter(x,y, c=c)
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


else:
	#print "hit"
	break_point = 0
	for i in range(0,steps):
	#while True:	
		
		
		z_a = False
		h_a = False
		time_passed = clock.tick(12)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()


		screen.blit(background,background_rect)

		if(counter == 0):
			x, y, c = first_step(everyone)
		else:	
			x, y, c = one_step(everyone)
			
			HMO[0,1:-1] = HMO[-2,1:-1]
			HMO[-1,1:-1] = HMO[1,1:-1]
			HMO[1:-1,0] = HMO[1:-1,-2]
			HMO[1:-1,-1] = HMO[1:-1,1]
			
			ZMO[0,1:-1] = ZMO[-2,1:-1]
			ZMO[-1,1:-1] = ZMO[1,1:-1]
			ZMO[1:-1,0] = ZMO[1:-1,-2]
			ZMO[1:-1,-1] = ZMO[1:-1,1]	

		
		pygame.display.flip()
		pygame.image.save(screen, 'pymovie/tmp%04d.png' % counter)
		
				


					
		#print "HMO 0",HMO

		
		counter += 1
	
		
		for j in c:
			if(j == 'r' or j =='w'):
				z_a = True
			if(j == 'b'):
				h_a = True

		if not z_a or not h_a:
			break_point += 1
			if break_point==10:
				break
		



#if makeplot: 
if makeplot:
	#sci.movie('pymovie/tmp*.png',encoder='ffmpeg',output_file=savefile,vcodec='libx264rgb',vbitrate='2400',qscale=1,fps=10)
	os.system('avconv -r 10 -i %s -vcodec libx264 %s' %('pymovie/tmp%04d.png',savefile))

	for filename in glob.glob('pymovie/tmp*.png'):
		os.remove(filename)



	
if makegraph:
	plt.plot(steps_array, zombie_array,'r',label='Zombies')
	plt.plot(steps_array, human_array,'b', label='Humans')
	plt.plot(steps_array, infected_array,'w', label='Infected')
	plt.plot(steps_array, dead_array,'k', label='Dead')
	plt.legend()

	plt.axis([0,steps,0,len(everyone)])
	plt.show()
	
