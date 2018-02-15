import numpy as np
import random

directions=np.array([[-1,0],[0,1],[1,0],[0,-1]])

class Vacuum_Cleaner:
    #current coordinate of vacuum_cleaner
    VC_x=2
    VC_y=2

    #field
    #0 - empty cell, 1 - garbish, 3 - VC
    field=np.zeros([5,5])
    field[VC_y, VC_x]=3

    def __init__(self):
        # current coordinate of vacuum_cleaner
        self.VC_x = 2
        self.VC_y = 2

        # field
        # 0 - empty cell, 1 - garbish, 3 - VC
        self.field = np.zeros([5, 5])
        self.field[self.VC_y, self.VC_x] = 3

    def check_move(self,a):
        if (abs(self.VC_y + a[0] - 2) > 2 or abs(self.VC_x + a[1] - 2) > 2):
            return False
        return True

    def move(self, a):
        if(self.check_move(a)==False):
            return False
        self.field[self.VC_y +a[0], self.VC_x+a[1]]=3
        self.field[self.VC_y, self.VC_x] =0
        self.VC_y+=a[0]
        self.VC_x+=a[1]


    def throw_garbage(self):
        t=True
        while(t):
            x=random.randint(0, 4)
            y=random.randint(0, 4)
            if(self.field[y, x]==0):
                t=False
                if(random.randint(0,3)==0):
                    self.field[y, x]=1

    def seen_garbage(self):
        t=False
        array=np.array([0,0])
        for i in range(len(directions)):
            try:
                if (self.field[self.VC_y +directions[i][0], self.VC_x+directions[i][1]]==1):
                    if(t==False):
                        t=True
                    array=np.vstack((array,directions[i]))
            except:
                pass
        if(t==False):
            for i in range(len(directions)):
                if(self.check_move(directions[i])):
                    if (t == False):
                        t = True
                    array = np.vstack((array, directions[i]))
        array = np.delete(array, 0, 0)
        return array

    def centre_distance(self,x,y):
        return (abs(x-2)**2+abs(y-2)**2)**(1/2)

    def centre_direction(self, array):
        best_i=array[0]
        best_dist=self.centre_distance(self.VC_y+array[0][0],self.VC_x+array[0][1])
        for i in range(1,len(array)):
            if(self.centre_distance(self.VC_y+array[i][0],self.VC_x+array[i][1])<best_dist):
                print("here we go", best_i)
                best_i = array[i]
                best_dist = self.centre_distance(self.VC_y+array[i][0],self.VC_x+array[i][1])
        print(best_i)
        return best_i

    def algorithm(self):
        for i in range(0,100):
            print(VC.field)
            self.move(self.centre_direction(self.seen_garbage()))
            self.throw_garbage()

    def count_garbage(self):
        sum=0
        for i in range(0,5):
            for j in range(0,5):
                if(self.field[i][j]==1):
                    sum+=1
        return sum



avarege =0
n=10
for i in range(0,n):
    VC = Vacuum_Cleaner()
    VC.algorithm()
    avarege+=VC.count_garbage()
print(avarege/n)
# print(VC.field)
