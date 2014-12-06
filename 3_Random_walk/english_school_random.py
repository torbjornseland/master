import matplotlib.pyplot as plt
from math import sqrt,pi,cos,sin,atan2
import os, sys,glob

import random as rd
import numpy as np


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
        old_x = self.x
        old_y = self.y
            
        self.direction = rd.uniform(0,2*pi)
        test_x = self.x + self.step*cos(self.direction) 
        test_y = self.y + self.step*sin(self.direction)

        #Through the wall
        """
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
        #Turn when hitting the wall
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

        SMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)
        

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
        
        old_x = self.x
        old_y = self.y

        susceptible_to_infected(self.x,self.y,self.HI)

        self.direction = rd.uniform(0,2*pi)         #New direction for the random walker
        test_x = self.x + self.step_x*cos(self.direction) 
        test_y = self.y + self.step_y*sin(self.direction)
     
        # Through the wall
        """
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
        """

        # Turn when reaching the wall
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
        
        #Change position in the matrix
        IMO.change_pos(old_x,old_y,self.x,self.y,self.my_id)

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
            #From infected to removed       
            if(e.color() == 'r'):
                removed_rand = rd.random()
                if (removed_rand < self.IR): #percent chance of beeing a Zombie
                    print "infected to removed"
                    x_cord, y_cord = e.coordinates()
                    IMO.delete_value(x_cord,y_cord,e.get_id())
                    everyone[counter] = removed(self.X,self.Y,e.get_id(),self.step,'m',self.grid_size)
                    if (IMO.get_amount() == 0):
                        print "All infected are removed, quit program"
                        sys.exit(0)

            #From susceptible to infected
            if(e.color() == 'w'):
                print "from susceptible to infected"
                x_cord, y_cord = e.coordinates()
                SMO.delete_value(x_cord,y_cord,e.get_id())
                IMO.set_value(x_cord,y_cord,e.get_id())
                everyone[counter] = infected(self.HI,self.X,self.Y,e.get_id(),self.step,'r',self.grid_size)

            e.update(everyone)
            p = e.coordinates()
            self.x[counter] = p[0]
            self.y[counter] = p[1]
            self.c[counter] = e.color()
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
        self.mat[i+1,j+1].append(id_)  #Infected matrix
        self.amount += 1
    
    def delete_value(self,x,y,id_):
        i,j = self.find_ij(x,y)
        count_pos = 0
        for val in self.mat[i+1,j+1]:
            if(val == id_):
                del self.mat[i+1,j+1][count_pos]
        count_pos += 1
        self.amount -= 1

    def get_matrix(self):
        return self.mat

    def find_ij(self,x,y):
        i = ((x*self.grid_size)/float(self.X)) 
        j = ((y*self.grid_size)/float(self.Y)) 
        if(i == self.grid_size):
            i -= 1
        if(j == self.grid_size):
            j -= 1
        return i,j
    
    def field_id(self,x,y):
        i,j = self.find_ij(x,y)
        group = []

        for k in range(3):
            for l in range(3):
                group.extend(self.mat[i+k,j+l])
        return group

    def change_pos(self,old_x,old_y,new_x,new_y,id_):
        self.delete_value(old_x,old_y,id_)
        self.set_value(new_x,new_y,id_)
    
    def get_amount(self):
        return self.amount

def susceptible_to_infected(i,j,HI):
        susceptible = SMO.field_id(i,j) 
        s_power = len(susceptible)
        if(s_power != 0):
            for k in range(s_power):
                human_infec = rd.random()
                if(human_infec < HI):
                    everyone[susceptible[k]].getcolor = 'w' #Human getting infected

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
    grid_size = 300
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
    SN = 621             #Susceptible number
    IN = 1             #Infected number

    HI = 2.18*10**(-3)*X**(2)*(1/float(24*60))
    #IR = 0.44036
    IR = 1-(0.55964**(1/float(24*60)))



    susceptible_ = []
    for id_ in range(0,SN):       #Making zombies
        s = susceptible(X,Y,id_,step,'b',grid_size)
        susceptible_.append(s)
        x,y = s.coordinates()
        if makepath:
            path_x.append(x)
            path_y.append(y)
        SMO.set_value(x,y,id_)

    infected_ = []
    for id_ in range(0,IN):       #Making zombies
        i_ = infected(HI,X,Y,id_+SN,step,'r',grid_size)
        infected_.append(i_)
        x,y = i_.coordinates()
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
    
