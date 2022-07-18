from pickletools import optimize
from typing import List
from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
from Model3D import*
from Model2D import*
from Settings import*
from copy import deepcopy as copy
import glob
import Optimizer

model3d: Model3D = None
model2d: Model2D = None
optimizer: Optimizer.Optimizer = None
objects: List


def loadObj(i=0):
    global OBJ_INDEX, model3d
    OBJ_INDEX = (OBJ_INDEX + i)%len(objects)
    model3d = Model3D(objects[OBJ_INDEX])

def init():
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(WINDOW_SIZE[0], WINDOW_SIZE[1])
    glutCreateWindow('BestPOV')
    glClearColor(*BACKGROUND_COLOR)
    glPolygonOffset(1.0,1.0)
    glLineStipple(*STIPPLE_STYLE)
    glLineWidth(LINE_WIDTH)
    
def resetGL():
    glColor4f(*BLACK)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

def drawString(position=1, text=''):
    glDisable(GL_DEPTH_TEST)
    glColor4fv(TEXT_COLOR)
    if position == 0: height = 700-SPACING
    else: height = 200-(SPACING*position)
    if height >= BOTTOM_MARGIN:
        glWindowPos2f(LEFT_MARGIN, height)
        for c in text:
            glutBitmapCharacter(FONT, ord(c))

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)
    resetGL()
    glViewport(0,200,500,500)
    mp = model3d.getProjectionMatrix()
    mv = model3d.getModelviewMatrix()
    model3d.draw()
    glViewport(500,200,500,500)
    resetGL()
    # model2d = Model2D(copy(model3d),mp,mv)
    if optimizer:
        model2d.draw()
        drawString(3, 'Profit: {}'.format(optimizer.best_profit))
    drawString(0, "{}".format(objects[OBJ_INDEX].split('\\')[-1][:-4]))
    drawString(1, "{} Projection".format(PROJECTIONS[model3d.projection]))
    drawString(2, 'Rho: {}\tTheta: {}º\tPhi: {}º'.format(*model3d.viewpoint))
    glutSwapBuffers()


""" USER INPUT FUNCTIONS """
def specialKeyFunction( key,x,y):
    if not optimizer:
        if   ( key == GLUT_KEY_LEFT ): model3d.viewpoint[1] = (model3d.viewpoint[1] + STEP_SIZE[1]) % 360
        elif ( key == GLUT_KEY_RIGHT ): model3d.viewpoint[1] = (model3d.viewpoint[1] - STEP_SIZE[1]) % 360
        elif ( key == GLUT_KEY_UP and model3d.viewpoint[2]<180): model3d.viewpoint[2] += STEP_SIZE[2]
        elif ( key == GLUT_KEY_DOWN and model3d.viewpoint[2]>0): model3d.viewpoint[2] -= STEP_SIZE[2]
        elif ( key == GLUT_KEY_HOME and model3d.viewpoint[0] > model3d.min_rho) : model3d.viewpoint[0] -= STEP_SIZE[0]
        elif ( key == GLUT_KEY_END and model3d.viewpoint[0] <= 2*model3d.min_rho): model3d.viewpoint[0] += STEP_SIZE[0]
        elif ( key == GLUT_KEY_PAGE_UP ): loadObj(-1)
        elif ( key == GLUT_KEY_PAGE_DOWN ): loadObj(+1)
        glutPostRedisplay()
def keyFunction(key,x,y):
    global optimizer
    if key.lower() == b'p' and not optimizer:
        model3d.projection = (model3d.projection + 1)%len(PROJECTIONS)
    if key.lower() == b's' and not optimizer:
        optimizer = Optimizer.SA(cost_fn,model3d.viewpoint,DOMAINS)
        glutIdleFunc(idle)
    if key.lower() == b't' and not optimizer:
        optimizer = Optimizer.TS(cost_fn,model3d.viewpoint,DOMAINS)
        glutIdleFunc(idle)
    if key == b' ' and optimizer:
        if optimizer.isRunning: optimizer.isRunning = False
        else: optimizer.isRunning = True
    if key == b'\r':
        if optimizer:
            optimizer = None
            glutIdleFunc(None)
        else: 
            loadObj()
    glutPostRedisplay()
        

def cost_fn(viewpoint):
    global model2d
    bg_model3=copy(model3d)
    bg_model3.viewpoint=viewpoint
    mp = bg_model3.getProjectionMatrix()
    mv = bg_model3.getModelviewMatrix()
    model2d = Model2D(bg_model3,mp,mv)
    glutPostRedisplay()
    return model2d.calculateProfit()

"""" IDLE FUNCTION """
def idle():
    global optimizer
    if optimizer.isRunning:
        if optimizer.step():
            model3d.viewpoint = optimizer.best_sol
        if optimizer.hasFinished():
            optimizer = None
            glutIdleFunc(None)
    glutPostRedisplay()

if __name__ == '__main__':
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyFunction)
    glutSpecialFunc(specialKeyFunction)
    glutIdleFunc(None)
    objects = glob.glob(OBJ_PATH + '*.obj')
    loadObj()
    glutMainLoop()