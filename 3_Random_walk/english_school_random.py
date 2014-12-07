import matplotlib.pyplot as plt
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np


class creature(object):

    def __init__(self,X,Y,x,y,id_,step,getcolor,grid_size):
        self.x = x 
        self.y = y 
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
        self.test_x = 0
        self.test_y = 0

    def update(self, everyone):
        c = 1

        if (self.no_steps == 0):
            self.direction = rd.uniform(0,2*pi)
            self.no_steps = 1 #rd.randint(1,20) 
        
        self.test_x = self.x + self.step*cos(self.direction) 
        self.test_y = self.y + self.step*sin(self.direction)
        self.stop_wall()

    def through_wall(self):
        if(self.test_x > self.X):
            self.x = self.test_x - self.X
        elif(self.test_x < 0):
            self.x = self.X + self.test_x
        else:
            self.x = self.test_x
        if(self.test_y > self.Y):
            self.y = self.test_y -self.Y
        elif(self.test_y < 0):
            self.y = self.Y + self.test_y
        else:
            self.y = self.test_y

    def stop_wall(self):
        if(self.test_x > self.X):
            self.x = 2*self.X- self.test_x
        elif(self.test_x < 0):
            self.x = - self.test_x
        else:
            self.x = self.test_x
        if(self.test_y > self.Y):
            self.y = 2*self.Y - self.test_y
        elif(self.test_y < 0):
            self.y = - self.test_y
        else:
            self.y = self.test_y
        
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

    def set_color(self,col):
        self.getcolor = col
    
    def coordinates(self):
        return (self.x, self.y)

    def color(self):
        return self.getcolor

class susceptible(creature):
    def __init__(self,*args):
        super(susceptible,self).__init__(*args)

    def update(self,everyone):
        old_x = self.x
        old_y = self.y
            
        self.direction = rd.uniform(0,2*pi)
        self.test_x = self.x + self.step*cos(self.direction) 
        self.test_y = self.y + self.step*sin(self.direction)
        
        self.stop_wall()
        SMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)
    
    def through_wall(self):
        super(susceptible,self).through_wall()   

    def stop_wall(self):
        super(susceptible,self).stop_wall()   

    def walk(self):
        super(susceptible,self).walk()

    def coordinates(self):
        return super(susceptible,self).coordinates()

    def set_color(self,col):
        return super(susceptible,self).set_color(col)

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
        
        old_x = self.x
        old_y = self.y

        susceptible_to_infected(self.x,self.y,self.HI)

        self.direction = rd.uniform(0,2*pi)         #New direction for the random walker
        self.test_x = self.x + self.step_x*cos(self.direction) 
        self.test_y = self.y + self.step_y*sin(self.direction)
        
        self.stop_wall() 
        
        IMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)

    def through_wall(self):
        super(infected,self).through_wall()   

    def stop_wall(self):
        super(infected,self).stop_wall()   

    def walk(self):
        super(infected,self).walk()

    def coordinates(self):
        return super(infected,self).coordinates()

    def set_color(self,col):
        return super(infected,self).set_color(col)

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

class run:
    def __init__(self,HI,IR,X,Y,step,grid_size,everyone):
        self.HI = HI
        self.IR = IR
        self.X = X
        self.Y = Y
        self.step = step
        self.grid_size = grid_size
        self.x = np.zeros(len(everyone))
        self.y = np.zeros(len(everyone))
        self.c = [0]*len(everyone)

    def one_step(self):
        counter = 0
        rem_num = 0
        inf_num = 0
        sus_num = 0
        for e in everyone:
            e.update(everyone)
            p = e.coordinates()
            self.x[counter] = p[0]
            self.y[counter] = p[1]
            self.c[counter] = e.color()
            counter += 1
        counter = 0
        for e in everyone:
            if(e.color() == 'r'):
                removed_rand = rd.random()
                if (removed_rand < self.IR): #percent chance of beeing a Zombie
                    print "infected to removed"
                    x_coord, y_coord = e.coordinates()
                    IMO.delete_value(x_coord,y_coord,e.get_id())
                    everyone[counter] = removed(self.X,self.Y,x_coord,y_coord,e.get_id(),self.step,'m',self.grid_size)
                    if (IMO.get_amount() == 0):
                        print SMO.get_matrix()
                        print IMO.get_matrix()
                        sys.exit(0)

            #From susceptible to infected
            if(e.color() == 'w'):
                print "susceptible to infected"
                x_coord, y_coord = e.coordinates()
                SMO.delete_value(x_coord,y_coord,e.get_id())
                IMO.set_value(x_coord,y_coord,e.get_id())
                everyone[counter] = infected(self.HI,self.X,self.Y,x_coord,y_coord,e.get_id(),self.step,'r',self.grid_size)
            counter += 1
        return self.x,self.y,self.c

    def first_step(self):
        counter = 0
        for e in everyone:
            p = e.coordinates()
            self.x[counter] = p[0]
            self.y[counter] = p[1]
            self.c[counter] = e.color()
        
            counter += 1
        return self.x,self.y,self.c

class matrix_constructor:
    def __init__(self,grid_size,X,Y):
        self.grid_size = grid_size
        self.mat = np.zeros([grid_size+2,grid_size+2],dtype=object) #Matrix
        for i in range(grid_size+2):
            for j in range(grid_size+2):
                self.mat[i,j] = [] 
        self.X = X
        self.Y = Y
        self.amount = 0

    def set_value(self,x,y,id_):
        i,j = self.find_ij(x,y)
        self.mat[i,j].append(id_)  #Infected matrix
        self.amount += 1
    
    def delete_value(self,x,y,id_):
        ok = False
        i,j = self.find_ij(x,y)
        count_pos = 0
        for val in self.mat[i,j]:
            if(val == id_):
                del self.mat[i,j][count_pos]
                self.amount -= 1
            count_pos += 1

    def get_matrix(self):
        return self.mat

    def get_matrix_block(self,x,y,i_range,j_range):
        i,j = self.find_ij(x,y)
        return self.mat[i-1:i+i_range-1,j-1:j+j_range-1]

    def find_ij(self,x,y):
        i_bas = int((x*self.grid_size)/float(self.X)) 
        j_bas = int((y*self.grid_size)/float(self.Y)) 
        if(i_bas == self.grid_size):
            i_bas -= 1
        if(j_bas == self.grid_size):
            j_bas -= 1
        return i_bas+1,j_bas+1
    
    def field_id(self,x,y,in_color):
        i,j = self.find_ij(x,y)
        group = []
        pos_group = []
        for k in range(-1,2):
            for l in range(-1,2):
                for per_id in self.mat[i+k,j+l]:
                    if (everyone[per_id].color() == in_color):
                        group.append(per_id)
                        pos_group.append([i+k,j+l]) 
        return group,pos_group

    def change_pos(self,old_x,old_y,new_x,new_y,id_):
        self.delete_value(old_x,old_y,id_)
        self.set_value(new_x,new_y,id_)
    
    def get_amount(self):
        return self.amount

def susceptible_to_infected(x,y,HI):
        susceptible_group, pos_group = SMO.field_id(x,y,'b') 
        s_power = len(susceptible_group)
        print "x",x
        print "y",y
        print SMO.get_matrix_block(x,y,3,3)
        print IMO.get_matrix_block(x,y,3,3)
        if(s_power != 0):
            raw_input("stop")
        if(s_power != 0):
            for k in range(s_power):
                human_infec = rd.random()
                if(human_infec < HI):
                    everyone[susceptible_group[k]].set_color('w') #Human getting infected 
                    SMO.delete_value(pos_group[k][0],pos_group[k][1],k)
                    print SMO.get_matrix_block(x,y,3,3)
                    print IMO.get_matrix_block(x,y,3,3)

#################Script##########################
#ZN, HN, steps, area_map, grid_size, ZK, HI, ZA, IZ, ID,makeplot, makegraph, savefile, mode = read_command_line()




    

if __name__ == '__main__':
    """
    IMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
    SMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Human matrix oldi
    for i in range(grid_size+2):
        for j in range(grid_size+2):
            IMO[i,j] = [] 
            SMO[i,j] = [] 
    """

    #General for english school
    grid_size = 100
    steps = 21600
    X = 100
    Y = 100
    step = 3.96

    IMO = matrix_constructor(grid_size,X,Y)
    SMO = matrix_constructor(grid_size,X,Y)

    grid_x = (X/float(grid_size))
    grid_y = (Y/float(grid_size))

    # Random position after 15 days
    """
    save_gap = 10
    print_plot = [1440,7200,21600]
    title_p = ['1 day', '5 days', '15 days']
    savename = ['plots/random_walk_1day.png' , 'plots/random_walk_5days.png', 'plots/random_walk_15days.png']
    makeplot = True
    makegraph = True 
    makepath = True
    savefile = "plots/english_school"
    SN = 1
    IN = 0
    HI = 2.18*10**(-3)
    IR = 0.44036
    path_x = []
    path_y = []
    """
    # English school simulation 
    save_gap = 10
    makeplot = False#True
    makegraph = True #False
    makepath = False
    savefile = "plots/english_school"
    SN = 20             #Susceptible number
    IN = 1             #Infected number

    HI = 2.18*10**(-3)*X**(2)*(1/float(24*60))
    #IR = 0.44036
    IR = 1-(0.55964**(1/float(24*60)))
    print "IR",IR



    susceptible_ = []
    for id_ in range(0,SN):       #Making zombies
        x = rd.randint(0,X)
        y = rd.randint(0,Y)
        s = susceptible(X,Y,x,y,id_,step,'b',grid_size)
        susceptible_.append(s)
        if makepath:
            path_x.append(x)
            path_y.append(y)
        SMO.set_value(x,y,id_)

    infected_ = []
    for id_ in range(0,IN):       #Making zombies
        x = rd.randint(0,X)
        y = rd.randint(0,Y)
        i_ = infected(HI,X,Y,x,y,id_+SN,step,'r',grid_size)
        infected_.append(i_)
        IMO.set_value(x,y,id_+SN)

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
    
    update = run(HI,IR,X,Y,step,grid_size,everyone)
    for i in range(0,steps):

        if (i%1000 == 0):
            print i

        if(counter == 0):
            x, y, c = update.first_step()
        else:
            x, y, c = update.one_step()    
    
        """
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
        """

        if (makeplot and (i%save_gap==0)):
            fig = plt.figure()
            #imgplot = plt.imshow(img)
            plt.scatter(x,y, c=c)
            plt.axis([0,X,0,Y])
            plt.savefig('moviefiles/tmp%04d.png' % (i/save_gap))
            plt.close()

        
        if makegraph:
            for e in everyone:
                if (e.color() == 'r' or e.color() == 'w'):
                    infected_array[i+1] = infected_array[i+1]+ 1
                elif (e.color() == 'b'):
                    susceptible_array[i+1] = susceptible_array[i+1]+ 1
                elif (e.color() == 'm'):
                    removed_array[i+1] = removed_array[i+1] + 1
                else:
                    print "ukjent",e.color()
        

        counter += 1

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
        plt.plot(steps_array, infected_array,'g', label='Infected')
        plt.plot(steps_array, removed_array,'r', label='Removed')
        plt.legend()

        plt.axis([0,steps,0,len(everyone)])
        plt.show()
    
