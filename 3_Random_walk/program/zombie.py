
import random
import pylab 
import time
from math import sqrt 

class zombie(object):
  def __init__(self,x,y):
    self.x = x 
    self.y = y 
    self.s = 0.1

  def update(self, everyone): 
    c = 1 
    dx = 0 
    dy = 0 
    for e in everyone: 
      if e.color() == "b":   
        mx, my = e.coordinates()
        r = sqrt((self.x - mx)**2 + (self.y - my)**2)
        if r < 0.2:  
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
    self.s = 0.2 

  def update(self, everyone): 

    c = 1 
    dx = 0 
    dy = 0 
    for e in everyone: 
      if e.color() == "r":   
        mx, my = e.coordinates()
        r = sqrt((self.x - mx)**2 + (self.y - my)**2)
        if r < 0.2:  
	  c += 1 
	  dx += mx - self.x  
	  dy += my - self.y 
        if r < 0.01:  
	  self.s = 0 

    dx /= c 
    dy /= c 
    self.x = self.x - self.s*dx 
    self.y = self.y - self.s*dy  


  def coordinates(self):
    return (self.x, self.y)

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
for i in range(0,ZN):  
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

for i in range(0, 100): 

  x, y, c = one_step(everyone)

  pylab.scatter(x,y, c=c)
  pylab.show()
  pylab.draw()
  pylab.update()


