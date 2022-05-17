import copy
import numpy as np
from Model import Model
import Profit as p
import bcolors as  b

class Model2d(Model):
    matrix = []     #PROYECTION MATRIX
    vP = []         #VERTEX PROYECTED
    profit = 0      #PROFIT

    def __init__(self, model, pMatrix, mvMatrix):
        self.V , self.vN, self.F, self.L, self.N, self.center, self.maxRadius, self.rho = model.V , model.vN, model.F, model.L, model.N, model.center, model.maxRadius, model.rho
        self.vP = self.getProjection(pMatrix,mvMatrix)
        self.profit = self.getProfit()


    def getProfit(self):
        crossed, near = p.count_crossed(self)
        clutter=p.count_node_collisions(self)
        area, ratio =p.total_area(self)
        print(b.WARN, "Crossed:" ,crossed, b.END)
        print(b.WARN, "Near:" ,near, b.END)
        print(b.WARN, "Clutter:" ,clutter, b.END)
        print(b.WARN, "Ratio:" ,ratio, b.END)
        print(b.WARN, "Area:" ,area, b.END,flush=True)
        profit = area*ratio
        penalty = crossed + clutter + near
        return profit - penalty

    def getProjection(self,pMatrix,mvMatrix):
        self.matrix = np.matmul(pMatrix,mvMatrix)   
        V2=copy.deepcopy(self.V)
        for v in V2: v.append(1)
        vP=[]
        for v in V2:
            mat=np.matmul(self.matrix,v)        #VERTEX PROYECTION
            vector=np.asarray(mat).reshape(-1)
            vector = vector/vector[3]           #VERTEX NORMALIZATION
            vP.append(vector)                   #ADD NORMALIZED VERTEX TO MATRIX VP
        
        return np.array(vP)  
