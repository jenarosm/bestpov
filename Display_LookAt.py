from turtle import clear
from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
from Model import *
from Model2d import *
import Draw as d
import os
import Optimizer


""" Declaramos las Variables Globales """
model,opt,projection, width, fovy, rho, theta, phi = Model,Optimizer.SA, 'pers',3, 45, 0, 0 , 90
running,pause = False, False

"""Inicialización del Proceso"""
def init(modelName):      
    global model, rho, opt
    model = Model("Obj/"+modelName+".obj")
    rho= model.getRho(fovy)
    opt=Optimizer.SA([rho,theta,phi])

    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_SINGLE|GLUT_RGB)
    glutInitWindowSize(500,500)
    glutInitWindowPosition(100,100)
    glutCreateWindow("PointOfView")

    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)   #SETTING UP TRANSPARENCY/ALPHA BLEND
    glEnable( GL_BLEND )
    glEnable(GL_CULL_FACE)                              #SETTING UP FACE CULLING FOR TRANSPARENCY
    glClearColor( 1, 1, 1, 1 )                          #BACKGROUND COLOR
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_POLYGON_OFFSET_FILL)
    glLineWidth(width)
    glPolygonOffset(1,1)
 
"""Glut Display Function"""
def display():
    global model2d
    pMatrix=d.getMProj(fovy, rho, projection)
    mvMatrix=d.getMRot(rho,theta,phi,model.center)
    d.draw3d(model,width)
    d.drawCoord()
    # glPopMatrix()
    # glutSwapBuffers()
    model2d = Model2d(model,pMatrix,mvMatrix)
    d.draw2d(model2d)
    profit=model2d.profit
    d.drawText(rho,theta,phi,profit) 
    glPopMatrix()
    glutSwapBuffers()
    
"""Special Key Function"""
def specialKeyFunction( key,x,y):                       
    global phi, theta, rho, width, model2d
    if ( key == GLUT_KEY_LEFT ):
        theta += 5
        if(theta>360):
            theta-=360
    elif ( key == GLUT_KEY_RIGHT ):
        theta -= 5
        if (theta<=0):
            theta+=360
    elif ( key == GLUT_KEY_UP):
        phi += 5
        if (phi>360):
            phi-=360
    elif ( key == GLUT_KEY_DOWN ):
        phi -= 5
        if (phi<=0):
            phi+=360
    elif ( key == GLUT_KEY_INSERT ):
        theta = phi = 0

    elif ( key == GLUT_KEY_HOME ):
        rho -= 0.5
        # width *= 1.25
    elif ( key == GLUT_KEY_END ):
        rho += 0.5
        # width /= 1.25
    # print(model2d.vP)
    glutPostRedisplay()

def keyboardCB(key,x,y):
    global running, projection, pause
    # print(key)
    if key == b'r': 
        running  = True
    if key == b'p':
        if projection == 'pers':
            projection = 'orto'
        elif projection == 'orto':
            projection = 'pers'
        glutPostRedisplay()
    if key == b' ':
        if pause : pause = False
        else: pause = True
        print("SPACEBAR")


"""Idle Function"""
def idle():
    global opt,rho,theta,phi, model2d, running
    if(not running): pass
    elif(pause): pass
    elif(not opt.hasFinished()):
        global rho,theta,phi, model2d
        rho,theta,phi=opt.step(model2d, [rho,theta,phi])
        glutPostRedisplay()
    elif (running):
        running = False
        rho,theta,phi=opt.getSol()
        glutPostRedisplay()
        print('He terminado')
        opt=Optimizer.SA([rho,theta,phi])

"""Main Function"""
def main():
    modelName=GUI()
    init(modelName)
    glutDisplayFunc(display)
    glutSpecialFunc(specialKeyFunction)
    glutKeyboardFunc(keyboardCB)
    glutIdleFunc(idle)
    glutMainLoop()

"""User Interface for Object Choice"""
def GUI():
    objects = ['Train','Hand','InwardCube','Hammer','Chair','Boat','Cheese','Cross','Cube','Diamond', 'HexPrism', 'House', 'Icosphere', 'Monkey', 'Piramid', 'TriPrism','Table', 'TruncPiramid', 'Weird']
    choice = -1
    while(int(choice)-1 not in range(len(objects))):
        try: os.system('cls')
        except: os.system('clear')
        print("\n-------- Choose Object: --------")
        for i ,object in enumerate(objects):
            print("{}.-{}".format(i+1,object))
        choice = input("\nEnter your choice: ")
        try: int(choice)
        except: choice = -1
    return objects[int(choice)-1]

main()