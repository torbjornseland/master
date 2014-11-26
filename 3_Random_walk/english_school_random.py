import matplotlib.pyplot as plt
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np


class creature(object):
    def __init__(self,X,Y,step,getcolor):
        self.x = rd.randint(0,X)
        self.y = rd.randint(0,Y)
        self.X = X
        self.Y = Y
        self.step = step
        self.getcolor = getcolor
        self.no_steps = 0
        self.direction = 0

    def update(self, everyone):
        c = 1

        if (self.no_steps == 0):
            self.direction = rd.uniform(0,2*pi)
            self.no_steps = 1 #rd.randint(1,20) 
        
        test_x = self.x + self.step*cos(self.direction) 
        test_y = self.y + self.step*sin(self.direction)
        self.no_steps -= 1  
        
        if(test_x > self.X):
            self.x = test_x - self.X
        elif(test_x < 0):
            self.x = self.X + test_x
        else:
            self.x = test_x
            
        if(test_y > self.Y):
            self.y = test_y -self.Y
        elif(test_y < 0):
            self.y = self.Y + test_y
        else:
            self.y = test_y

    def walk(self):
        if rd.random() > 0.5:
            self.x += self.step
        else:
            self.x -= self.step
        
        if rd.random() > 0.5:
            self.y += self.step
        else:
            self.y -= self.step
    def get_pos(self):
        return self.x,self.y
    
    def coordinates(self):
        return (self.x, self.y)

    def color(self):
        return self.getcolor

class susceptible(creature):
    def __init__(self,*args):
        super(susceptible,self).__init__(*args)

    def update(self,everyone):
        super(susceptible,self).update(everyone)

    def walk(self):
        super(susceptible,self).walk()

    def coordinates(self):
        return super(susceptible,self).coordinates()

    def color(self):
        return super(susceptible,self).color()

class infected(creature):
    def __init__(self,*args):
        super(infected,self).__init__(*args)

    def update(self,everyone):
        super(infected,self).update(everyone)

    def walk(self):
        super(infected,self).walk()

    def coordinates(self):
        return super(infected,self).coordinates()

    def color(self):
        return super(infected,self).color()

class removed(creature):
    def __init__(self,*args):
        super(removed,self).__init__(*args)

    def update(self,everyone):
        super(removed,self).update(everyone)

    def walk(self):
        super(removed,self).walk()

    def coordinates(self):
        return super(removed,self).coordinates()

    def color(self):
        return super(removed,self).color()


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
        """
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
        
        if(e.color() == 'c'):   #getting infected
            everyone[counter] = infected(p[0],p[1],e.get_id(),screen,'w','pictures/infected.png')
        if(e.color() == 'm'):   #dying to dead
            everyone[counter] = dead(p[0],p[1],e.get_id(),screen,'k','pictures/tombstone.png')
    

        
        e.blitme()
        """
        counter += 1
        
    
    return x,y,c

def first_step(everyone):
    for e in everyone:
        p = e.coordinates()
        x.append(p[0])
        y.append(p[1])
        c.append(e.color())
    
    return x,y,c

#################Script##########################
#ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile, mode = read_command_line()

steps = 100
makeplot = True
makegraph = True
savefile = "plots/english_school"
SN = 10
IN = 10
X = 20
Y = 20
step = 0.1

susceptible_ = []
for i in range(0,SN):       #Making zombies
    s = susceptible(X,Y,step,'b')
    susceptible_.append(s)

infected_ = []
for i in range(0,IN):       #Making zombies
    i_ = infected(X,Y,step,'r')
    infected_.append(i_)

everyone = susceptible_ + infected_ 
x = []
y = []
c = []

#files = []

counter = 0

steps_array = np.linspace(0,steps,steps+1) 
susceptible_array = np.zeros(steps+1)
infected_array = np.zeros(steps+1)
removed_array = np.zeros(steps+1)

susceptible_array[0] = len(susceptible_)
infected_array[0] = len(infected_)

for i in range(0,steps):

    if(counter == 0):
        x, y, c = first_step(everyone)
    else:
        x, y, c = one_step(everyone)    
    
    if makeplot:
        fig = plt.figure()
        #imgplot = plt.imshow(img)
        plt.scatter(x,y, c=c)
        plt.axis([0,X,0,Y])
        plt.savefig('moviefiles/tmp%04d.png'% counter)
        plt.close()

    
    if makegraph:
        for e in everyone:
            if (e.color() == 'r'):
                infected_array[i+1] = infected_array[i+1]+ 1
            elif (e.color() == 'b'):
                susceptible_array[i+1] = susceptible_array[i+1]+ 1
            else:
                removed_array[i+1] = removed_array[i+1] + 1
    

    counter += 1

if makeplot:
    #sci.movie('pymovie/tmp*.png',encoder='ffmpeg',output_file=savefile,vcodec='libx264rgb',vbitrate='2400',qscale=1,fps=10)
    #os.system('avconv -r 10 -i %s -vcodec libx264 %s' %('moviefiles/tmp%04d.png',savefile))
    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm -y' %('moviefiles/tmp%04d.png',savefile))

    for filename in glob.glob('moviefiles/tmp*.png'):
        os.remove(filename)



    
if makegraph:
    plt.plot(steps_array, susceptible_array,'r',label='Susceptible')
    plt.plot(steps_array, infected_array,'b', label='Infected')
    plt.plot(steps_array, removed_array,'k', label='Removed')
    plt.legend()

    plt.axis([0,steps,0,len(everyone)])
    plt.show()
    
