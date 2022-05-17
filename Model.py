from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import numpy as np

class Model:
    V = []  #VERTEX
    vN= []  #VERTEX NORMALS
    F = []  #FACES
    L = []  #LINES
    N = []  #NORMALS
    center = [0,0,0]
    maxRadius = 0.0
    rho = 0

    def __init__(self,filename):
        with open(filename, 'r') as file:       #LOAD FILE
            for line in file:   #READ FILE
                aux=[]

                if(line.split()[0]=='v'):       #LOAD VERTEX
                    for i in line.split():
                        if(i!='v'): aux.append(float(i)) 
                    self.V.append(aux)
                
                if(line.split()[0]=='vn'):      #LOAD VERTEX NORMALS
                    for i in line.split():
                        if(i!='vn'): aux.append(float(i))    
                    self.vN.append(aux)
                   
                if(line.split()[0]=='f'):       #LOAD FACES AND FACE NORMALS
                    auxf=[]
                    auxvn=[]
                    auxn=[]

                    for i in line.split():
                        
                        str=i.split("/")    #REGEX FOR FACES WITHOUT TEXTURE MAPS
                        if(str):
                            if len(str) == 3:
                                auxf.append(int(str[0]))    #LOAD FACE ONTO AUXILIARY ARRAY
                                auxvn=int(str[2])           #LOAD FACE VERTEX NORMALS ONTO AUXILIARY ARRAY

                            if len(str) == 2:
                                auxf.append(int(str[0]))
                                auxvn=int(str[1])

                    if auxvn : auxn=self.vN[auxvn-1]    #LOAD FACE NORMALS ONTO AUXILIARY ARRAY
                    
                    self.F.append(auxf)
                    self.N.append(auxn)

            self.linesInit()            
            self.centerInit()
            self.mRadiusInit()
            file.close()

    def linesInit(self):
        self.L = [] #RESET LINES
        auxL   = [] #AUX LINES

        for face in self.F:
            for x in range(0,len(face)):
                
                auxL.append( [face[x-1]-1 , face[x]-1 ]) 

        for i in range(len(auxL)): #REMOVE DUPLICATES
            dupe=False
            for j in range(i+1,len(auxL)):
                if ( (auxL[i][0]==auxL[j][1]) and (auxL[i][1]==auxL[j][0]) ): 
                    dupe=True
                    break
                elif ( (auxL[i][0]==auxL[j][0]) and (auxL[i][1]==auxL[j][1]) ): 
                    dupe=True
                    break
            if (dupe==False): self.L.append(auxL[i])

    def centerInit(self):
        self.center=(np.amax(self.V, axis=0) + np.amin(self.V,axis=0)) / 2  #GET THE CENTER OF THE OBJECT

    def mRadiusInit(self):
        maxLength = 0.0
        distance = 0.0
        for vertex in self.V:
            distance=np.sqrt((vertex[0]-self.center[0])**2 + (vertex[1]-self.center[1])**2 + (vertex[2]-self.center[2])**2)
            if distance > maxLength:
                maxLength = distance            #GET THE MAXIMUM RADIUS

        self.maxRadius=maxLength
    def getRho(self, fovy):
        rho= (self.maxRadius/2 / np.tan(fovy/2*np.pi/180))+(2*self.maxRadius)   #CALCULATE RHO BASED ON MODEL
        return round(rho,0)
