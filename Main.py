from pickletools import optimize
from typing import List
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
from Model3D import *
from Model2D import *
from Settings import *
from copy import deepcopy as copy
import glob
import Optimizer

""" GLOBAL VARIABLES """
model3d: Model3D = None
model2d: Model2D = None
optimizer: Optimizer.Optimizer = None
object_list: List

""" AUXILIARY FUNCTIONS """
def loadObj(i=0):
    global OBJ_INDEX, model3d
    OBJ_INDEX = (OBJ_INDEX + i)%len(object_list)
    model3d = Model3D(object_list[OBJ_INDEX])

def drawString(position=1, text='', column=0):
    glDisable(GL_DEPTH_TEST)
    glColor4fv(TEXT_COLOR)
    if position == -1: height = 700-SPACING
    else: height = 200-(SPACING*position)
    if height >= BOTTOM_MARGIN:
        glWindowPos2f(LEFT_MARGIN+(500*column), height)
        for c in text:
            glutBitmapCharacter(FONT, ord(c))

""" PROGRAM INITIALIZATION """
def init():
    """ Object Loading """
    global object_list
    object_list = glob.glob(OBJ_PATH + '*.obj')
    loadObj()
    """ Glut and OpenGL """
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(*WINDOW_SIZE)
    glutCreateWindow('BestPOV')
    glClearColor(*BACKGROUND_COLOR)
    glPolygonOffset(1.0,1.0)
    glLineStipple(*STIPPLE_STYLE)
    glLineWidth(LINE_WIDTH)

""" DISPLAY FUNCTION """
def display():
    global model3d, model2d
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glEnable(GL_DEPTH_TEST)

    glViewport(0,200,500,500)
    mp, mv = model3d.draw()
    if optimizer:
        glViewport(500,200,500,500)
        model2d.draw()
        if(optimizer.isRunning):
            drawString(0, "Running optimizer...")
        else:
            drawString(0, "Optimizer paused!")
        drawString(1, optimizer.status(),0)

        drawString(-1, "T/S - Start \t\t SPACE - Pause \t\t ENTER - Stop",1)
        drawString(0, "Area:{} Front:{} Back:{} V_Rep: {}".format(model2d.area,model2d.front,model2d.back,round(model2d.vertex_repulsion,2)),1)
        drawString(1, "Tight: {} Crossed: {} P_Rep: {}".format(round(model2d.tight_angles,2),round(model2d.crossing_edges,2),round(model2d.parallel_repulsion,2)),1)
        drawString(3, "{} Projection".format(PROJECTIONS[model3d.projection_type]),1)
        drawString(4, 'Rho: {}\tTheta: {}º\tPhi: {}º'.format(*np.round(model2d.viewpoint)),1)
        drawString(5, "Profit: {}".format(round(model2d.profit,2)),1)
    else: 
        model2d=Model2D(copy(model3d),mp,mv)
        model3d.profit=model2d.calculateProfit()
        drawString(0, "T/S - Start \t\t SPACE - Pause \t\t ENTER - Reset")
        drawString(1, "ARROWS - Rotate \t\t PgUp/PgDn - Cycle \t\t P - Change Projection")
    drawString(-1, "{}".format(object_list[OBJ_INDEX].split('\\')[-1][:-4]))
    drawString(3, "{} Projection".format(PROJECTIONS[model3d.projection_type]))
    drawString(4, 'Rho: {}\tTheta: {}º\tPhi: {}º'.format(*np.round(model3d.viewpoint,3)))
    drawString(5, "Profit: {}".format(round(model3d.profit,2)))
    # drawString(4, "Area:{} Front:{} Back:{} V_Rep: {}".format(model3d.projection.area,model3d.projection.front,model3d.projection.back,round(model3d.projection.vertex_repulsion,2)))
    # drawString(5, "Tight: {} Crossed: {} P_Rep: {}".format(round(model3d.tight_angles,2),round(model3d.crossing_edges,2),round(model3d.parallel_repulsion,2)))
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
        if(key): model3d.profit = None
        glutPostRedisplay()
def keyFunction(key,x,y):
    global optimizer
    if key.lower() == b'p' and not optimizer:
        model3d.projection_type = (model3d.projection_type + 1)%len(PROJECTIONS)
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
        
""" PROFIT CALCULATION """
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
    global optimizer, model2d
    if optimizer.isRunning:
        if optimizer.step():
            model3d.viewpoint = optimizer.best_sol
            model3d.profit = optimizer.best_profit
            model3d.projection = copy(model2d)
        if optimizer.hasFinished():
            optimizer = None
            glutIdleFunc(None)
    glutPostRedisplay()

""" MAIN LOOP """
if __name__ == '__main__':
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(keyFunction)
    glutSpecialFunc(specialKeyFunction)
    glutIdleFunc(None)
    glutMainLoop()