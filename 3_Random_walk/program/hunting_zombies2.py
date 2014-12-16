
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
        parser.add_argument('--savedata',  type=str,
                    default='data', help='Name and path to the movie',
                    metavar='savedata')
        
        return parser

def read_command_line():
    parser = define_command_line_options()
    args = parser.parse_args()
    print 'ZN={}, HN={}, Steps={}, area={}, grid_size={},\nzombie_kill={}, human_infected={}, zombie_awake={},\ninfected_zombie={}, infected_dead={}, makeplot={},\nmakegraph={}, savefile={}, mode={}, savedata={}'.format(
        args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile, args.mode,args.savedata)
    return args.ZN, args.HN, args.S, args.area, args.g, args.ZK, args.HI, args.ZA, args.IZ, args.ID, args.makeplot, args.makegraph, args.savefile, args.mode, args.savedata

class creature(object):
    def __init__(self,step_x,step_y,x,y,my_id,screen,getcolor,img_creature,img_w,img_h,HI,IZ,ID,ZA,ZK):
        self.x = x
        self.y = y
        self.my_id = my_id
        self.screen = screen
        self.no_steps = 0
        self.getcolor = getcolor
        self.direction = 0
        self.HI = HI
        self.IZ = IZ
        self.ID = ID
        self.ZA = ZA
        self.ZK = ZK
        self.step_x = step_x
        self.step_y = step_y

        if self.screen != 0:
            self.base_image = pygame.image.load(img_creature).convert_alpha()
            self.image = self.base_image
            self.image_w, self.image_h = self.image.get_size()
        self.img_h = img_h
        self.img_w = img_w
        self.test_x = 0
        self.test_y = 0

    def through_wall(self):
        if(self.test_x > self.img_w):
            self.x = self.test_x - self.img_w
        elif(self.test_x < 0):
            self.x = self.img_w + self.test_x
        else:
            self.x = self.test_x
        if(self.test_y > self.img_h):
            self.y = self.test_y -self.img_h
        elif(self.test_y < 0):
            self.y = self.img_h + self.test_y
        else:
            self.y = self.test_y

    def stop_wall(self):
        if(self.test_x > self.img_w):
            self.x = 2*self.img_w- self.test_x
        elif(self.test_x < 0):
            self.x = - self.test_x
        else:
            self.x = self.test_x
        if(self.test_y > self.img_h):
            self.y = 2*self.img_h - self.test_y
        elif(self.test_y < 0):
            self.y = - self.test_y
        else:
            self.y = self.test_y

    def coordinates(self):
        return (self.x, self.y)

    def color(self):
        return self.getcolor
    
    def set_color(self,col):
        self.getcolor = col

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
    def __init__(self,min_size,*args):
        super(zombie,self).__init__(*args)
        self.dx = 0
        self.dy = 0
        self.same_room = 0
        self.min_size = min_size
    def update(self, everyone,ph_val):
        r_min = self.min_size
        mx_min = 0
        my_min = 0
        mx_way = 1
        my_way = 1
        
        old_x = self.x
        old_y = self.y
        
        fight_susceptible_vs_zombie(self.x,self.y,self.HI[ph_val],self.ZK[ph_val],self.get_id())

        if(self.getcolor == 'r'): 
            #Checking the mode
            if(mode[ph_val] == 'hunting' or mode[ph_val] == 'moving_smart'):
                for e in everyone:          #Run through all objects
                    if e.color() == "b":    #Checking if the object is blue
                        mx, my = e.coordinates()    #Returing the coordinate for the element
                        
                        if(abs(self.x-mx) <= self.img_w/2.):
                            x_way = -1
                            x_dir = self.x-mx
                        else:
                            x_way = 1
                            if((self.x-mx)<0):
                                x_dir = -1*(self.img_w-abs(self.x-mx))
                            else:
                                x_dir = self.img_w-abs(self.x-mx)
                        
                        if(abs(self.y-my) <= self.img_h/2.):
                            y_way = -1
                            y_dir = self.y-my
                        else:
                            if((self.y-my)<0):
                                y_dir = -1*(self.img_h-abs(self.y-my))
                            else:
                                y_dir = (self.img_h-abs(self.y-my))
                            y_way = 1

                    
                        #print "x_dir",x_dir
                        r = sqrt((x_dir)**2 + (y_dir)**2)
                        if area_free:
                            if (r < r_min and img[my][mx][0] != free_area):
                                r_min = r
                                mx_min = x_dir
                                my_min = y_dir
                                mx_way = x_way
                                my_way = y_way
                        else:    
                            if (r < r_min):
                                r_min = r
                                mx_min = x_dir
                                my_min = y_dir
                                mx_way = x_way
                                my_way = y_way
                if (r_min < self.min_size and r_min!= 0):
                    self.dx = (mx_min)/float(r_min)*mx_way
                    self.dy = (my_min)/float(r_min)*my_way
                    
                    self.test_x = self.x + self.step_x*self.dx
                    self.test_y = self.y + self.step_y*self.dy
                    self.through_wall()
                    if (area_free and (img[self.y][self.x][0] == free_area)):
                        self.min_size = r_min
                        self.dx = 0
                        self.dy = 0
                    self.direction = atan2((self.step_y*self.dy),(self.step_x*self.dx))
                else:
                    self.dx = 0
                    self.dy = 0
                

            if(mode[ph_val] == 'random' or (mode[ph_val] == 'moving_smart' and r_min == self.min_size)):
                if (self.no_steps == 0):
                    self.direction = rd.uniform(0,2*pi)
                    self.no_steps = rd.randint(1,20)
                    
        
                self.test_x = self.x + self.step_x*cos(self.direction) 
                self.test_y = self.y + self.step_y*sin(self.direction)
                self.through_wall()
                while (area_free and (img[self.y][self.x][0] == free_area)):
                    self.direction = rd.uniform(0,2*pi)
                    self.test_x = self.x + self.step_x*cos(self.direction) 
                    self.test_y = self.y + self.step_y*sin(self.direction)
                    self.through_wall()
                    

                self.no_steps -= 1
            ZMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)
   
    def through_wall(self):
        super(zombie,self).through_wall()   

    def stop_wall(self):
        super(zombie,self).stop_wall()   
         
    def coordinates(self):
        return super(zombie,self).coordinates()

    def color(self):
        return super(zombie,self).color()

    def set_color(self,col):
        return super(zombie,self).set_color(col)

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

    def get_same_room(self):
        return self.same_room

    def increase_same_room(self):
        self.same_room += 1

class man(creature):
    def __init__(self,min_size,*args):
        super(man,self).__init__(*args)
        self.min_size = min_size

    def update(self, everyone,ph_val):

        c = 1
        dx = 0
        dy = 0
        hyp = 0
        old_x = self.x
        old_y = self.y

        test_x = self.x
        test_y = self.y
        
        i = int(self.x*grid_size/self.img_w)
        j = int(self.y*grid_size/self.img_h)
        
        if(mode[ph_val] == 'moving_smart' or mode[ph_val] == 'hunting'):
            for e in everyone:
                if e.color() == "r":    #Checking if the object is a zombie
                    mx, my = e.coordinates()
                    if(abs(self.x-mx) <= self.img_w/8.):
                        x_way = -1
                        x_dir = self.x-mx
                    else:
                        if((self.x-mx)<0):
                            x_dir = -1*(self.img_w-abs(self.x-mx))
                        else:
                            x_dir = self.img_w-abs(self.x-mx)
                        x_way = 1
                        
                    if(abs(self.y-my) <= self.img_h/8.):
                        y_way = -1
                        y_dir = self.y-my
                    else:
                        if((self.y-my)<0):
                            y_dir = -1*(self.img_h-abs(self.y-my))
                        else:
                            y_dir = (self.img_h-abs(self.y-my))
                        y_way = 1

                    
                    r = sqrt((x_dir)**2 + (y_dir)**2)
                    
                    if r < (self.min_size*0.5):
                        dx += (self.min_size*0.5-r)*x_dir
                        dy += (self.min_size*0.5-r)*y_dir
                        mx_way = x_way
                        my_way = y_way
            
            hyp = sqrt(dx**2 + dy**2)   
        
            if(hyp != 0):
                dx = dx/float(hyp)*mx_way
                dy = dy/float(hyp)*my_way
            if((dx != 0 or dy != 0) or mode[ph_val]=='hunting'):
                self.test_x = self.x - self.step_x*dx #Checking if x is inside the map    
                self.test_y = self.y - self.step_y*dy #Checking if y is inside the map
                
                self.direction = atan2((self.step_y*dy),(self.step_x*dx))+pi
        if(mode[ph_val] == 'random' or (mode[ph_val]=='moving_smart' and hyp == 0)) :
            if (self.no_steps == 0):
                self.direction = rd.uniform(0,2*pi)
                self.no_steps = rd.randint(1,20) 
        
            self.test_x = self.x + self.step_x*cos(self.direction) 
            self.test_y = self.y + self.step_y*sin(self.direction)
            self.no_steps -= 1  
                
            
        if attack:
            self.test_x = self.x
            self.test_y = self.y 
        #Sending them through the wall
        self.through_wall()
        
        #Giving the human/infected a new position
        HMO.change_pos(old_x,old_y,self.x,self.y,self.get_id())
    
    def through_wall(self):
        super(man,self).through_wall()   

    def stop_wall(self):
        super(man,self).stop_wall()   
    
        
    def coordinates(self):
        return (self.x,self.y)

    def set_color(self,col):
        return super(man,self).set_color(col)

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
    
    def update(self, everyone,ph_val):
        c = 1

    def coordinates(self):
        return (self.x, self.y)

    def color(self):
        return self.getcolor

    def set_color(self,col):
        return super(dead,self).set_color(col)
    
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

    def update(self, everyone,ph_val):
        c = 1
        old_x = self.x
        old_y = self.y
        if (self.no_steps == 0):
            self.direction = rd.uniform(0,2*pi)
            self.no_steps = 1 #rd.randint(1,20) 
        
        self.test_x = self.x + self.step_x*cos(self.direction) 
        self.test_y = self.y + self.step_y*sin(self.direction)
        self.no_steps -= 1  
        
        self.through_wall()
        IMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)

    def through_wall(self):
        super(infected,self).through_wall()   

    def stop_wall(self):
        super(infected,self).stop_wall()   

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
    
class run:
    def __init__(self,min_size,HI,IZ,ID,ZA,ZK,img_w,img_h,step_x,step_y,grid_size,everyone,phases):
        self.HI = HI
        self.IZ = IZ
        self.ID = ID
        self.ZA = ZA
        self.ZK = ZK
        self.img_w = img_w
        self.img_h = img_h
        self.step_x = step_x
        self.step_y = step_y
        self.grid_size = grid_size
        self.x = np.zeros(len(everyone))
        self.y = np.zeros(len(everyone))
        self.c = [0]*len(everyone)
        self.i = 0
        self.j = 0
        self.breakLoop = False
        self.phases = phases
        self.ph_val = 0
        self.min_size = min_size
    
    def one_step(self,everyone,step_nr):
        counter = 0
        for i in range(len(self.phases)):
            if (step_nr < self.phases[i]):
                self.ph_val = i
                break
        for e in everyone:
            mx = e.coordinates()
            #print "mx",mx[0]
            #print "my",mx[1]
            e.update(everyone,self.ph_val)
            p = e.coordinates()
            #print "after mx",p[0]
            #print "after my",p[1]

            self.x[counter] = p[0]
            self.y[counter] = p[1]
            self.c[counter] = e.color()


            counter += 1
        #print "HMO"
        #print HMO.get_matrix()
        #print "ZMO"
        #print ZMO.get_matrix()
        #print "IMO"
        #print IMO.get_matrix()
        #raw_input()
        counter = 0
        for e in everyone:
            #infected
            if(e.color() == 'w'):
                inf_rand = rd.random()
                if (inf_rand < self.IZ[self.ph_val]): #percent chance of beeing a Zombie
                    ex,ey = e.coordinates()
                    IMO.delete_value(ex,ey,e.get_id())
                    everyone[counter] = zombie(self.min_size,self.step_x,self.step_y,ex,ey,e.get_id(),screen,'r','pictures/zombie.png',self.img_w,self.img_h,self.HI,self.IZ,self.ID,self.ZA,self.ZK)
                    ZMO.set_value(ex,ey,e.get_id())
                elif(inf_rand < (self.IZ[self.ph_val]+self.ID[self.ph_val])):#percent change of dying 
                    ex,ey = e.coordinates()
                    IMO.delete_value(ex,ey,e.get_id())
                    everyone[counter] = dead(self.step_x,self.step_y,ex,ey,e.get_id(),screen,'k','pictures/tombstone.png',self.img_w,self.img_h,self.HI,self.IZ,self.ID,self.ZA,self.ZK)
                else:
                    pass
        
            #dead       
            if(e.color() == 'k'):
                dead_rand = rd.random()
                if (dead_rand < self.ZA[self.ph_val]): #percent chance of beeing a Zombie
                    ex,ey = e.coordinates()
                    everyone[counter] = zombie(self.min_size,self.step_x,self.step_y,ex,ey,e.get_id(),screen,'r','pictures/zombie.png',self.img_w,self.img_h,self.HI,self.IZ,self.ID,self.ZA,self.ZK)
                    ZMO.set_value(ex,ey,e.get_id())
                else:
                    pass
            
            if(e.color() == 'c'):   #getting infected
                #print "id is getting infected",e.get_id()
                ex,ey = e.coordinates()
                HMO.delete_value(ex,ey,e.get_id())
                everyone[counter] = infected(self.step_x,self.step_y,ex,ey,e.get_id(),screen,'w','pictures/infected.png',self.img_w,self.img_h,self.HI,self.IZ,self.ID,self.ZA,self.ZK)
                IMO.set_value(ex,ey,e.get_id())
            if(e.color() == 'm'):   #dying to dead
                ex,ey = e.coordinates()
                ZMO.delete_value(ex,ey,e.get_id())
                everyone[counter] = dead(self.step_x,self.step_y,ex,ey,e.get_id(),screen,'k','pictures/tombstone.png',self.img_w,self.img_h,self.HI,self.IZ,self.ID,self.ZA,self.ZK)
        

            if screen != 0: 
                e.blitme()  
            counter += 1
            
        
        return self.x,self.y,self.c

    def first_step(self,everyone):
        counter = 0
        for e in everyone:
            p = e.coordinates()
            self.x[counter] = p[0]
            self.y[counter] = p[1]
            self.c[counter] = e.color()
        
            counter += 1
        return self.x,self.y,self.c

class matrix_constructor:
    def __init__(self,grid_size,img_w,img_h):
        self.grid_size = grid_size
        self.mat = np.zeros([grid_size+2,grid_size+2],dtype=object) #Matrix
        for i in range(grid_size+2):
            for j in range(grid_size+2):
                self.mat[i,j] = [] 
        self.img_w = img_w
        self.img_h = img_h
        self.amount = 0

    def set_value(self,x,y,id_):
        self.i,self.j = self.find_ij(x,y)
        self.mat[self.i,self.j].append(id_)  #Infected matrix
        self.amount += 1
    
    def delete_value(self,x,y,id_):
        ok = False
        #print "x",x
        #print "y",y
        self.i,self.j = self.find_ij(x,y)
        count_pos = 0
        for val in self.mat[self.i,self.j]:
            if(val == id_):
                del self.mat[self.i,self.j][count_pos]
                self.amount -= 1
            count_pos += 1

    def get_matrix(self):
        return self.mat

    def get_matrix_block(self,x,y,i_range,j_range):
        self.i,self.j = self.find_ij(x,y)
        if (i_range == 0 and j_range == 0):
            return self.mat[self.i,self.j]
        else:
            return self.mat[self.i-1:self.i+i_range-1,self.j-1:self.j+j_range-1]

    def find_ij(self,x,y):
        i_bas = int((x*self.grid_size)/float(self.img_w)) 
        j_bas = int((y*self.grid_size)/float(self.img_h)) 
        if(i_bas == self.grid_size):
            i_bas -= 1
        if(j_bas == self.grid_size):
            j_bas -= 1
        return i_bas+1,j_bas+1
    
    def field_id(self,x,y,in_color):
        self.i,self.j = self.find_ij(x,y)
        group = []
        pos_group = []
        for k in range(-1,2):
            for l in range(-1,2):
                for per_id in self.mat[self.i+k,self.j+l]:
                    if (everyone[per_id].color() == in_color):
                        group.append(per_id)
                        pos_group.append(everyone[per_id].coordinates()) 
        return group,pos_group

    def change_pos(self,old_x,old_y,new_x,new_y,id_):
        self.delete_value(old_x,old_y,id_)
        self.set_value(new_x,new_y,id_)
    
    def get_amount(self):
        return self.amount

def fight_susceptible_vs_zombie(x,y,HI,ZK,zombie_id):
        #susceptible_group, pos_group = SMO.field_id(x,y,'b') 
        #i,j = SMO.find_ij(x,y)
        #susceptible_group = list(SMO.get_matrix_block(x,y,0,0))
        zombie_group = list(ZMO.get_matrix_block(x,y,0,0)) 
        human_group = list(HMO.get_matrix_block(x,y,0,0)) 
        s_power = len(human_group)
        ca = 1
        if attack:
            ca = s_power
        if(s_power != 0):
            for k in range(s_power):
                #everyone[0].increase_same_room()
                #print "same room nr",everyone[0].get_same_room()
                human_infec = rd.random()
                zombie_killed = rd.random()
                if(human_infec < HI):
                    e = everyone[human_group[k]]
                    e.set_color('c') #Human getting infected 
                    s_x,s_y = e.coordinates()
                    HMO.delete_value(s_x,s_y,human_group[k])
                if(zombie_killed < ZK*ca):
                    everyone[zombie_id].set_color('m')     #Zombie is dying
                    ZMO.delete_value(x,y,zombie_id)
                    break
                    


#############################--Script--#####################################



def run_blindern():
    beta = [0.01155,0.000011];rho=[0.0137,0.015];alpha=[0.00044,0.000208];
    q = 621/float(98.64) #Average number of meetings during one minute
    HI = []
    ZK = []
    IZ = [0.0137,0.015]
    ID = [0,0]
    ZA = [0,0]
    for i in range(2):
        HI.append(beta[i]*q) 
        ZK.append(alpha[i]*q)
        #IZ.append(1-(1-rho[i])**(1/float(100)))

    global screen
    phases = [300,steps]
    if game_on:
        pygame.init()       

        background = pygame.image.load('pictures/Blindern2.jpg')
        background_size = background.get_size()
        background_rect = background.get_rect()
        screen = pygame.display.set_mode(background_size)
        background = background.convert()
        clock = pygame.time.Clock()
    else:
        screen = 0



    global img_h
    global img_w
    global img
    global free_area
    img = mpimg.imread('pictures/Blindern2.jpg')
    img_h,img_w,c = img.shape
    min_size = min(img_h,img_w)*0.3
    free_area = img[img_h-1][img_w-1][0] #White Blindern    

    grid_x = (img_w/float(grid_size))
    grid_y = (img_h/float(grid_size))

    step_length = 0.83/4 #The distance per 1/100 minute

    step_x = grid_x*step_length
    step_y = grid_y*step_length

    global ZMO
    global HMO
    global IMO
    ZMO = matrix_constructor(grid_size,img_w,img_h)
    HMO = matrix_constructor(grid_size,img_w,img_h)
    IMO = matrix_constructor(grid_size,img_w,img_h)
    M_emp = matrix_constructor(grid_size,img_w,img_h)

    """
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
    """

    zombies = []
    for i in range(0,ZN):       #Making zombies
        x_start = rd.randint(0,grid_size-1)
        y_start = rd.randint(0,grid_size-1)
        
        x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
        
        z = zombie(min_size,step_x,step_y,x,y,i,screen,'r','pictures/zombie.png',img_w,img_h,HI,IZ,ID,ZA,ZK)
        zombies.append(z)
        ZMO.set_value(x,y,i)
        #ZMO[x_start+1,y_start+1].append(i)  #Zombie matrix old



    men = []
    first = True
    if (spread == "uniform"):
        for i in range(0,HN):
            x_start = rd.randint(0,grid_size-1)
            y_start = rd.randint(0,grid_size-1)

            x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
            m = man(min_size,step_x,step_y,x,y,i+ZN,screen,'b','pictures/redhead.png',img_w,img_h,HI,IZ,ID,ZA,ZK)
            men.append(m)
            HMO.set_value(x,y,i+ZN)
    elif (spread == 'gaussian'):
        small = 21
        medium = 200
        for i in range(0,HN):
            if (i < small):
                g_x = 6*(grid_size/float(40))
                g_y = 6*(grid_size/float(40))
                x_start = rd.gauss(g_x,4.08)            
                y_start = rd.gauss(g_y,4.08)            
            elif(i < small+medium):
                g_x = 12*(grid_size/float(40))
                g_y = 25*(grid_size/float(40))
                x_start = rd.gauss(g_x,3.25)            
                y_start = rd.gauss(g_y,3.25)            
            else:
                g_x = 25*(grid_size/float(40))
                g_y = 12*(grid_size/float(40))
                x_start = rd.gauss(g_x,3.98)            
                y_start = rd.gauss(g_y,3.98)            

            if x_start < 0:
                x_start = 0
            if y_start < 0:
                y_start = 0
            if x_start > grid_size-1:
                x_start = grid_size-1
            if y_start > grid_size-1:
                y_start = grid_size-1
            
            x, y = x_start*img_w/float(grid_size), y_start*img_h/float(grid_size) 
            m = man(min_size,step_x,step_y,x,y,i+ZN,screen,'b','pictures/redhead.png',img_w,img_h,HI,IZ,ID,ZA,ZK)
            men.append(m)
            HMO.set_value(x,y,i+ZN)

    global everyone
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

    update = run(min_size,HI,IZ,ID,ZA,ZK,img_w,img_h,step_x,step_y,grid_size,everyone,phases)
    
    global attack
    attack = False

    if not game_on: 
            for i in range(0,steps):
                if (i % 100 == 0):
                    print "nr:",i

                if (i == 3300):
                    print "attacking"
                    attack = True
                if (i == 3350):
                    print "stop counter attack"
                    attack = False
                    
    
                if(counter == 0):
                    x, y, c = update.first_step(everyone)
                else:
                    x, y, c = update.one_step(everyone,i)    
                    
                    HMO.mat[0,1:-1] = HMO.mat[-2,1:-1]
                    HMO.mat[-1,1:-1] = HMO.mat[1,1:-1]
                    HMO.mat[1:-1,0] = HMO.mat[1:-1,-2]
                    HMO.mat[1:-1,-1] = HMO.mat[1:-1,1]
                    
                    ZMO.mat[0,1:-1] = ZMO.mat[-2,1:-1]
                    ZMO.mat[-1,1:-1] = ZMO.mat[1,1:-1]
                    ZMO.mat[1:-1,0] = ZMO.mat[1:-1,-2]
                    ZMO.mat[1:-1,-1] = ZMO.mat[1:-1,1]  
                if makeplot:
                    fig = plt.figure()
                    imgplot = plt.imshow(img)
                    plt.scatter(x,y, c=c)
                    plt.savefig('moviefiles/tmp%05d.png'% counter)
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
                
                if ((zombie_array[i+1] == 0 and infected_array[i+1] == 0) or human_array[i+1] == 0):
                    infected_array[i+2:] = infected_array[i+1] 
                    human_array[i+2:] = human_array[i+1] 
                    dead_array[i+2:] = dead_array[i+1] 
                    zombie_array[i+2:] = zombie_array[i+1] 
                    print "break loop"
                    break

                counter += 1


    else:
        #print "hit"
        break_point = 0
        for i in range(0,steps):
        #while True:    
            
            if (i % 100 == 0):
                print "nr:",i
             
            z_a = False
            h_a = False
            time_passed = clock.tick(12)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()


            screen.blit(background,background_rect)
            if (i == 3300):
                print "attacking"
                attack = True
            if (i == 3350):
                print "stop counter attack"
                attack = False

            if(counter == 0):
                x, y, c = update.first_step(everyone)
            else:   
                x, y, c = update.one_step(everyone,i)
                
                HMO.mat[0,1:-1] = HMO.mat[-2,1:-1]
                HMO.mat[-1,1:-1] = HMO.mat[1,1:-1]
                HMO.mat[1:-1,0] = HMO.mat[1:-1,-2]
                HMO.mat[1:-1,-1] = HMO.mat[1:-1,1]
                
                ZMO.mat[0,1:-1] = ZMO.mat[-2,1:-1]
                ZMO.mat[-1,1:-1] = ZMO.mat[1,1:-1]
                ZMO.mat[1:-1,0] = ZMO.mat[1:-1,-2]
                ZMO.mat[1:-1,-1] = ZMO.mat[1:-1,1]  

            
            pygame.display.flip()
            pygame.image.save(screen, 'pymovie/tmp%05d.png' % counter)
            
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
        os.system('avconv -r 10 -i %s -vcodec libx264 %s.mp4' %('pymovie/tmp%05d.png',savefile))
        #os.system('avconv -r 10 -i %s -vcodec libvpx %s.webm -y' % ('pymovie/tmp%05d.png',savefile))

        for filename in glob.glob('pymovie/tmp*.png'):
            os.remove(filename)



    print "make graph"    
    if makegraph:
        plt.plot(steps_array, human_array,'b', label='Susceptible')
        plt.plot(steps_array, infected_array,'g', label='Infected')
        plt.plot(steps_array, zombie_array,'r',label='Zombies')
        plt.plot(steps_array, dead_array,'c', label='Removed')
        plt.legend()
        plt.axis([0,steps,0,len(everyone)])
        #plt.show()
    return human_array,infected_array, zombie_array, dead_array

ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile, mode, savedata = read_command_line()
game_on = False #False
mode = ['moving_smart','moving_smart']
spread = 'uniform'
area_free = False
sim_failed = 0
first_sim = True
N = 100
N_ok = 0
random_steps = steps
susceptible_matrix = np.zeros([N,random_steps+1])
infected_matrix = np.zeros([N,random_steps+1])
zombie_matrix = np.zeros([N,random_steps+1])
removed_matrix = np.zeros([N,random_steps+1])

steps_array = np.zeros(random_steps+1)
#sus = np.zeros(random_steps)
#inf = np.zeros(random_steps)
#zom = np.zeros(random_steps)
#rem = np.zeros(random_steps)

tot_num = 0
for i in range(N):
    print "number:",i
    sus,inf,zom,rem = run_blindern()
    for j in range(random_steps+1):
        susceptible_matrix[i,j] = sus[j]
        infected_matrix[i,j] = inf[j]
        zombie_matrix[i,j] = zom[j] 
        removed_matrix[i,j] = rem[j]
    #print susceptible_matrix
    #print infected_matrix
    #print zombie_matrix
    #print removed_matrix

    np.save('data/susceptible_matrix_%s.npy' % savedata,susceptible_matrix)
    np.save('data/infected_matrix_%s.npy' % savedata,infected_matrix)
    np.save('data/zombie_matrix_%s.npy' % savedata,zombie_matrix)
    np.save('data/removed_matrix_%s.npy' % savedata,removed_matrix)

