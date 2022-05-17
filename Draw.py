from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import numpy as np
from numpy import sin
from numpy import cos
from numpy.lib import tracemalloc_domain
import bcolors as b

rad=np.pi/180

"""GET PROJECTION MATRIX"""
def getMProj(fovy,rho,projection):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()

    if  projection == 'orto':
        glOrtho(-rho/2,rho/2,-rho/2,rho/2, 0,50)
    elif projection == 'pers':
        gluPerspective(fovy, 1, 0.1, 50)

    pMatrix = np.matrix(glGetFloatv(GL_PROJECTION_MATRIX))      #GET PROJECTION MATRIX
    pMatrix = pMatrix.transpose()

    return pMatrix

"""GET MODELVIEW MATRIX"""
def getMRot(rho,theta,phi,center):
    glMatrixMode(GL_MODELVIEW)

    glLoadIdentity()
    glPushMatrix()
    
    tRad=theta*rad
    pRad=phi*rad
    
    if (phi<=180):
        gluLookAt(rho*sin(tRad)*sin(pRad),  rho*cos(pRad), rho*cos(tRad)*sin(pRad), 0,0,0, 0,1,0)
    else:
        gluLookAt(rho*sin(tRad)*sin(pRad),  rho*cos(pRad), rho*cos(tRad)*sin(pRad), 0,0,0, 0,-1,0)
        

    glTranslatef(-center[0],-center[1],-center[2])


    mvMatrix = np.matrix(glGetFloatv(GL_MODELVIEW_MATRIX))      #GET MODELVIEW MATRIX
    mvMatrix = mvMatrix.transpose()

    return mvMatrix

"""DRAW 3D MODEL"""
def draw3d(model,width):
    glViewport(0,0,500,500)
    glClear( GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT )
#----------------- DRAW THE LINES LOOP ----------------
    glLineWidth(width)
    glDisable(GL_POLYGON_OFFSET_FILL)
    for face in model.F:
        glColor4f(0,0,0,1)
        glBegin(GL_LINE_LOOP)           #DRAW THE LINES
        #glBegin(GL_TRIANGLE_FAN)
        for vertex in face:
            glVertex3dv(model.V[vertex-1], 0)

        glEnd()

#----------------- DRAW THE FACES LOOP ----------------
    glEnable(GL_POLYGON_OFFSET_FILL)
    for face in model.F:
        glColor4f(0.5,0.9,1,0.9)        #COLOR AND ALPHA
        #glBegin(GL_LINE_LOOP)
        glBegin(GL_TRIANGLE_FAN)        #DRAW THE FACES
        for vertex in face:
            glVertex3dv(model.V[vertex-1], 0)

        glEnd()
    glDisable(GL_POLYGON_OFFSET_FILL)  

"""DRAW 2D MODEL"""
def draw2d(model2d):
    glViewport(500,0,500,500)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluOrtho2D(-1,1,-1,1)
    glMatrixMode(GL_MODELVIEW)
    glLineWidth(1)
    glLoadIdentity()
    # glPushMatrix()

    glDisable(GL_POLYGON_OFFSET_FILL)
    for line in model2d.L:
        glColor4f(0,0,0,1)
        glBegin(GL_LINE_LOOP) #DRAW THE LINES
        glVertex2dv(model2d.vP[line[0]][0:2])
        glVertex2dv(model2d.vP[line[1]][0:2])
        glEnd()

"""DRAW COORDINATE SYSTEM"""
def drawCoord():
    glViewport(0,400,100,100)
    glLineWidth(2)
    glColor4f(1,0,0,1)
    glBegin(GL_LINE_LOOP)
    glVertex3dv([0,0,0], 0)
    glVertex3dv([1.5,0,0], 0)
    glEnd()
    glColor4f(0,1,0,1)
    glBegin(GL_LINE_LOOP)
    glVertex3dv([0,0,0], 0)
    glVertex3dv([0,1.5,0], 0)
    glEnd()
    glColor4f(0,0,1,1)
    glBegin(GL_LINE_LOOP)
    glVertex3dv([0,0,0], 0)
    glVertex3dv([0,0,1.5], 0)
    glEnd()

"""TEXT ON SCREEN"""
def drawText(rho,theta,phi,penalty):
    glViewport(0,0,500,500)
    position=str("Rho=" + str(rho) + " Theta=" + str(theta) + " Phi=" + str(phi) )
    label(-9,-9,5, "Profit={:.2f}".format(penalty))
    label(-9,-8,5, position)
    # glPopMatrix()
    # glutSwapBuffers()  

"""GLUT TEXT """
def label(x, y, z, s):
    '''takes string input and outputs it to OpenGl Environment'''
    glPushMatrix()
    x=x/10
    y=y/10
    glTranslatef(x, y, 0.0)
    scale=z/10000
    glScalef(scale,scale,scale)
    for c in s:
        glutStrokeCharacter(GLUT_STROKE_ROMAN, ord(c))
        glTranslatef(20, 0.0, 0.0)
    glPopMatrix()
