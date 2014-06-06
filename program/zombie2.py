import random
import pylab
#from scitools.std import *
import time
from math import sqrt

import os, sys


class zombie(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.s = 0.1

	def update(self, everyone):
		c = 1
		dx = 0
		dy = 0
		for e in everyone:			#Run through all objects
			if e.color() == "b":	#Checking if the object is blue
				mx, my = e.coordinates()	#Returing the coordinate for the element
				r = sqrt((self.x -mx)**2 + (self.y -my)**2)
				if r < 0.2: # Checking the distance to the human, if it is closer than 0.2, the zombie will go towards the human
					c += 1
					dx += mx - self.x
					dy += my - self.y
			
		dx /= c
		dy /= c

		self.x = self.x + self.s*dx
		self.y = self.y + self.s*dy

	def coordinates(self):
		return (self.x, self.y)

	def color(self):
		return "r"

class man(object):
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.s = 0.2	# Speed
		

	def update (self, everyone):

		c = 1
		dx = 0
		dy = 0
		for e in everyone:
			if e.color() == "r":	#Checking if the object is a zombie
				mx, my = e.coordinates()
				r = sqrt((self.x - mx)**2 + (self.y - my)**2)
				if r < 0.2:
					c += 1
					dx += mx - self.x
					dy += my - self.y
				if r < 0.01:	# if it is closer than 0.01 the human will stop moving
					self.s = 0
		dx /= c
		dy /= c
		self.x = self.x - self.s*dx
		self.y = self.y - self.s*dy

	def coordinates(self):
		return (self.x,self.y)

	def color(self):
		return "b"

def one_step(everyone):
	for e in everyone:
		e.update(everyone)
		p = e.coordinates()
		x.append(p[0])
		y.append(p[1])
		c.append(e.color())
	
	return x,y,c

ZN = 100
zombies = []
for i in range(0,ZN):		#Making zombies
	x, y = random.random(), random.random()
	z = zombie(x,y)
	zombies.append(z)

MN = 7
men = []
first = True
for i in range(0,MN):
	x, y = random.random(), random.random()
	m = man(x,y)
	men.append(m)


everyone = zombies + men
x = []
y = []
c = []

pylab.hold(False)

files = []


for i in range(0,5):

	x, y, c = one_step(everyone)
	pylab.scatter(x,y, c=c)
	#pylab.show()
	print "kommer den hit"
	pylab.clf()
	
	for e in everyone:
		e.update(everyone)


