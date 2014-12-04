import matplotlib.pyplot as plt
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np


class creature(object):
    def __init__(self,X,Y,id_,step,getcolor):
        self.x = rd.randint(0,X)
        self.y = rd.randint(0,Y)
        self.X = X
        self.Y = Y
        self.my_id = id_
        self.step_x = step
        self.step_y = step
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
        
        """
        #Through the wall
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
        """
        if(test_x > self.X):
            self.x = 2*self.X- test_x
        elif(test_x < 0):
            self.x = - test_x
        else:
            self.x = test_x

        if(test_y > self.Y):
            self.y = 2*self.Y - test_y
        elif(test_y < 0):
            self.y = - test_y
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
    
    def get_id(self):
        return self.my_id
    
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
    def __init__(self,HI,*args):
        super(infected,self).__init__(*args)
        self.HI = HI
    def update(self,everyone):
        #r_min = min_size
        #mx_min = 0
        #my_min = 0
        #mx_way = 1
        #my_way = 1
        
        test_x = self.x
        test_y = self.y
        
        i = int(self.x*grid_size/X)
        j = int(self.y*grid_size/Y)
        
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
                #del HMO[i+k,j+l][:] #Only allowed to do one battle each round

        #Fighting
        z_power = len(Zombie_force)
        h_power = len(Human_force)
        #print "h_power",h_power
        print "z_power",z_power
       
        if(h_power != 0):
            for k in range(h_power):
                human_infec = rd.random()
                if(human_infec < (self.HI+0.0*z_power)):
                    everyone[Human_force[k]].getcolor = 'r' #Human getting infected

                                        

        if(self.getcolor == 'r'): 
            if (self.no_steps == 0):
                self.direction = rd.uniform(0,2*pi)
                self.no_steps = rd.randint(1,20)
    
            test_x = self.x + self.step_x*cos(self.direction) 
            test_y = self.y + self.step_y*sin(self.direction)
            self.no_steps -= 1
         
    
    
            #Removing zombie from position  
            count_pos = 0
            for k in ZMO[i+1,j+1]:
                if(k == self.my_id):
                    del ZMO[i+1,j+1][count_pos]
                count_pos += 1

            if(test_x > X):
                self.x = test_x -X
            elif(test_x < 0):
                self.x = X + test_x
            else:
                self.x = test_x
            
            if(test_y > Y):
                self.y = test_y -Y
            elif(test_y < 0):
                self.y = Y + test_y
            else:
                self.y = test_y
                
            #Giving the zombie a new position
            i = int(self.x*grid_size/X)
            j = int(self.y*grid_size/Y)
            ZMO[i+1,j+1].append(self.my_id)
            #print "each round ZMN", ZMN    

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

save_gap = 10
steps = 21600
print_plot = [1440,7200,21600]
title_p = ['1 day', '5 days', '15 days']
savename = ['plots/random_walk_1day.png' , 'plots/random_walk_5days.png', 'plots/random_walk_15days.png']
makeplot = False #True
makegraph = False
savefile = "plots/english_school"
SN = 1
IN = 0
X = 100
Y = 100
step = 3.96
grid_size = 10
HI = 0.5 
path_x = []
path_y = []

grid_x = (X/float(grid_size))
grid_y = (Y/float(grid_size))

ZMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
ZMN = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
for i in range(grid_size+2):
    for j in range(grid_size+2):
        ZMO[i,j] = [] 
        ZMN[i,j] = [] 

HMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Human matrix old
for i in range(grid_size+2):
    for j in range(grid_size+2):
        HMO[i,j] = [] 


susceptible_ = []
for id_ in range(0,SN):       #Making zombies
    s = susceptible(X,Y,id_,step,'b')
    susceptible_.append(s)
    x,y = s.coordinates()
    path_x.append(x)
    path_y.append(y)
    x_start =int((x*grid_size)/X) 
    print x_start
    y_start =int((y*grid_size)/Y) 
    HMO[x_start+1,y_start+1].append(id_)  #Zombie matrix old

infected_ = []
for id_ in range(0,IN):       #Making zombies
    i_ = infected(HI,X,Y,id_+SN,step,'r')
    infected_.append(i_)
    x,y = i_.coordinates()
    print "x",x
    x_start =int((x*grid_size)/X) 
    y_start =int((y*grid_size)/Y) 
    print "x_start",x_start
    print "id",id_ + SN
    ZMO[x_start+1,y_start+1].append(id_+SN)  #Zombie matrix old

print "start HMO", HMO
print "start ZMO", ZMO
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

    #print ZMO
    if (i%save_gap==0):
        path_x.append(x[0])
        path_y.append(y[0])
    for j in range(len(print_plot)):
        if print_plot[j] == i:
            plt.plot(path_x, path_y, 'o')
            plt.axis([0,X,0,Y])
            plt.title(title_p[j])
            plt.savefig(savename[j])
            plt.show()


    if (makeplot and (i%save_gap==0)):
        fig = plt.figure()
        #imgplot = plt.imshow(img)
        plt.scatter(x,y, c=c)
        plt.axis([0,X,0,Y])
        plt.savefig('moviefiles/tmp%04d.png' % (i/save_gap))
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
makepath = True
if makepath:
    plt.plot(path_x, path_y, 'o')
    plt.axis([0,X,0,Y])
    plt.title(title_p[-1])
    plt.savefig(savename[-1])
    plt.show()

if makeplot:
    #sci.movie('pymovie/tmp*.png',encoder='ffmpeg',output_file=savefile,vcodec='libx264rgb',vbitrate='2400',qscale=1,fps=10)
    #os.system('avconv -r 10 -i %s -vcodec libx264 %s' %('moviefiles/tmp%04d.png',savefile))
    os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm -y' %('moviefiles/tmp%04d.png',savefile))

    for filename in glob.glob('moviefiles/tmp*.png'):
        os.remove(filename)



    
if makegraph:
    plt.plot(steps_array, susceptible_array,'b',label='Susceptible')
    plt.plot(steps_array, infected_array,'r', label='Infected')
    plt.plot(steps_array, removed_array,'k', label='Removed')
    plt.legend()

    plt.axis([0,steps,0,len(everyone)])
    #plt.show()
    
