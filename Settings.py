from multiprocessing.pool import INIT
from OpenGL.GL import*
from OpenGL.GLUT import*

"""Static Variables"""
PERSPECTIVE = 0
ORTHONORMAL = 1
PROJECTIONS = ['Perspective', 'Orthonormal']

"""Basic Colors"""
WHITE = [1,1,1,1]
BLACK = [0,0,0,1]
GREY = [0.3,0.3,0.3,1]
BLUE = [0.5,0.9,1,0.8]
YELLOW = [1,0.9,0.5,0.8]
RED = [1,0.5,0.5,0.8]

"""Object Settings"""
OBJ_PATH = 'Obj/'
OBJ_INDEX = 2
LINE_COLOR = BLACK
FACE_COLOR = BLUE
BACKGROUND_COLOR = WHITE
LINE_WIDTH = 2
STIPPLE_STYLE = [1, 0x00FF]

"""Initial Viewpoint Settings"""
INIT_THETA = 0
INIT_PHI = 90
INIT_FOVY = 60

""" Font Settings"""
TEXT_COLOR = BLACK
FONT =  GLUT_BITMAP_HELVETICA_18  #type: ignore
LEFT_MARGIN = 30
BOTTOM_MARGIN = 20
SPACING = 30

""" Window Arrangement Settings """
WINDOW_SIZE = [1000, 700]
LEFT_PANE = [0,200,500,500]
RIGHT_PANE = [500,200,500,500]

""" Optimizer Settings """
STEP_SIZE = [0.5,5,5]
DOMAINS = [[0,0],[0,360],[0,180]]

""" Profit Settings """
T = 0.1
TOP_VIEW = [20, 90]
TOP_VIEW_MULTIPLIER = 0.6

""" Auxiliary Functions """
isBetween= lambda x,d : d[0]<=x<=d[1]
def reset_matrices():
    glColor4f(*BLACK)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()


