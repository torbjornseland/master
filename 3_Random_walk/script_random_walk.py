from english_school_random import *

grid_size = 10
ZMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
ZMN = np.zeros([grid_size+2,grid_size+2],dtype=object) #Zombie matrix old
HMO = np.zeros([grid_size+2,grid_size+2],dtype=object) #Human matrix oldi
for i in range(grid_size+2):
    for j in range(grid_size+2):
        ZMO[i,j] = [] 
        ZMN[i,j] = [] 
        HMO[i,j] = [] 

def get_ZMO():
    return ZMO

def set_ZMO(ZMO):
    ZMO = ZMO

def get_HMO():
    return HMO

def set_HMO(HMO):
    HMO = HMO

if __name__ == '__main__':
    #General for english school
    steps = 3
    X = 100
    Y = 100
    step = 3.96


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
    makegraph = False
    makepath = False
    savefile = "plots/english_school"
    SN = 5             #Susceptible number
    IN = 5             #Infected number

    HI = 0.5#2.18*10**(-3)
    IR = 0.44036



    susceptible_ = []
    for id_ in range(0,SN):       #Making zombies
        s = susceptible(X,Y,id_,step,'b',grid_size)
        susceptible_.append(s)
        x,y = s.coordinates()
        if makepath:
            path_x.append(x)
            path_y.append(y)
        x_start =int((x*grid_size)/X) 
        print x_start
        y_start =int((y*grid_size)/Y) 
        HMO[x_start+1,y_start+1].append(id_)  #Zombie matrix old

    infected_ = []
    for id_ in range(0,IN):       #Making zombies
        i_ = infected(HI,X,Y,id_+SN,step,'r',grid_size)
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
    
    update = run(HI,X,Y,step,grid_size,everyone)
    for i in range(0,steps):

        if(counter == 0):
            x, y, c = update.first_step()
        else:
            x, y, c = update.one_step()    


        #print ZMO
        print "runde: ",i
        print "HMO",HMO
        print "ZMO",ZMO
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
                if (e.color() == 'r'):
                    infected_array[i+1] = infected_array[i+1]+ 1
                elif (e.color() == 'b'):
                    susceptible_array[i+1] = susceptible_array[i+1]+ 1
                else:
                    removed_array[i+1] = removed_array[i+1] + 1
        

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
        plt.plot(steps_array, infected_array,'r', label='Infected')
        plt.plot(steps_array, removed_array,'k', label='Removed')
        plt.legend()

        plt.axis([0,steps,0,len(everyone)])
        plt.show()
