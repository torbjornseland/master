import matplotlib.pyplot as plt
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np

from script_random_walk import get_ZMO, set_ZMO, get_HMO, set_HMO


class creature(object):

    def __init__(self,X,Y,id_,step,getcolor,grid_size):
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
        self.grid_size = grid_size

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
        
        i = int(self.x*self.grid_size/self.X)
        j = int(self.y*self.grid_size/self.Y)
        
        if(i == self.grid_size):
            print "inne her"
            i = 0
        if(j == self.grid_size):
            print "inne j"
            j = 0
        
        Zombie_force = [] 
        Human_force = [] 

        ZMO = get_ZMO()
        HMO = get_HMO()
        print "---------------"
        print "id",self.my_id
        print ZMO

        for k in range(3):
            for l in range(3):
                Zombie_force.extend(ZMO[i+k,j+l])
                Human_force.extend(HMO[i+k,j+l])
                #del HMO[i+k,j+l][:] #Only allowed to do one battle each round

        #Fighting
        z_power = len(Zombie_force)
        h_power = len(Human_force)
        #print "h_power",h_power
        #print "z_power",z_power
       
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


            if(test_x > self.X):
                self.x = test_x -self.X
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
                
            #Giving the zombie a new position
            i = int(self.x*self.grid_size/self.X)
            j = int(self.y*self.grid_size/self.Y)
            ZMO[i+1,j+1].append(self.my_id)
            print ZMO
            
            set_ZMO(ZMO)

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
    x = np.zeros(len(everyone))
    y = np.zeros(len(everyone))
    c = [0]*len(everyone)
    counter = 0
    for e in everyone:
        p = e.coordinates()
        x[counter] = p[0]
        y[counter] = p[1]
        c[counter] = e.color()
    
        counter += 1
    return x,y,c

#################Script##########################
#ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile, mode = read_command_line()

    
