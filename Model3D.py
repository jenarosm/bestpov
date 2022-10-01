from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
from Settings import*
import numpy as np

""" Overwrite for multiple inputs """
glEnable = lambda *args: [OpenGL.GL.glEnable(i) for i in args]
glDisable = lambda *args: [OpenGL.GL.glDisable(i) for i in args]

""" Auxiliary Functions """
getCenter = lambda vertex: (np.amax(vertex, axis=0) + np.amin(vertex,axis=0)) / 2
getDistance = lambda v, c: np.sqrt((v[0]-c[0])**2 + (v[1]-c[1])**2 + (v[2]-c[2])**2)
getRadius = lambda vertex, center: np.amax([getDistance(v,center) for v in vertex])
getRho = lambda radius, fovy: round((radius / np.tan(fovy/2*np.pi/180)) + (radius/2),0)

def getLines(faces):
    lines = []
    for face in faces:
        for v in range(-1,len(face)-1):
            lines.append([face[v],face[v+1]])
    lines = [np.sort(l) for l in lines]
    return np.unique(lines, axis=0)

def polar2Cartesian(v3):
    rho, theta, phi =v3[0], np.deg2rad(v3[1]), np.deg2rad(v3[2])
    if phi == 0: phi = 1e-10
    return rho*np.sin(theta)*np.sin(phi) , rho*np.cos(phi), rho*np.cos(theta)*np.sin(phi)

def drawPolygons(model, color = BLACK, mode = GL_LINE, capabilities=None):
    glColor4fv(color)
    glPolygonMode(GL_FRONT_AND_BACK , mode)
    if capabilities: glEnable(*capabilities)
    for face in model.faces:
        glBegin(GL_POLYGON)
        for v in face:
            glVertex3fv(model.vertex[v-1])
        glEnd()
    if capabilities: glDisable(*capabilities)

class Model3D:
    
    def __init__(self,filename):
        global DOMAINS
        self.vertex = []
        self.faces = []
        self.load(filename)
        self.lines = getLines(self.faces)
        self.center = getCenter(self.vertex)
        self.radius = getRadius(self.vertex,self.center)
        self.fovy = INIT_FOVY  
        self.min_rho = getRho(self.radius, self.fovy)
        self.viewpoint = [self.min_rho, INIT_THETA, INIT_PHI]
        self.profit = None
        DOMAINS[0] = [self.min_rho,self.min_rho*2]
        self.projection_type = PERSPECTIVE   
    

    def load(self, filename):
        with open(filename, 'r') as file:
            for line in file:
                line = line.split()
                #Load Vertices
                if line[0] == 'v':
                    self.vertex.append([float(v) for v in line[1:]])
                #Load Faces
                if line[0] == 'f':
                    self.faces.append([int(f.split('/')[0]) for f in line[1:]])
            file.close

    def getProjectionMatrix(self):
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        if(self.projection_type == PERSPECTIVE):
            gluPerspective(self.fovy, 1, 0.1, 50)
        elif(self.projection_type == ORTHONORMAL):
            rho = self.viewpoint[0]
            glOrtho(-rho/2,rho/2,-rho/2,rho/2, 0, 50)
        return np.matrix(glGetFloatv(GL_PROJECTION_MATRIX)).transpose()

    def getModelviewMatrix(self):
        glMatrixMode(GL_MODELVIEW)
        glLoadIdentity()
        gluLookAt(*polar2Cartesian(self.viewpoint),0,0,0,0,1,0)
        glTranslatef(*-self.center)
        return np.matrix(glGetFloatv(GL_MODELVIEW_MATRIX)).transpose()

    
    def draw(self):
        reset_matrices()
        """ Get Matrices """
        mp = self.getProjectionMatrix()
        mv = self.getModelviewMatrix()
        """ Draw Stipple Lines """
        drawPolygons(self, LINE_COLOR, GL_LINE, [GL_LINE_STIPPLE])
        """ Draw Faces """
        drawPolygons(self, FACE_COLOR, GL_FILL, [GL_BLEND, GL_CULL_FACE, GL_POLYGON_OFFSET_FILL])
        """ Draw Front Lines """
        drawPolygons(self, LINE_COLOR, GL_LINE)
        reset_matrices()
        return mp, mv

if __name__=='__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    WndId = glutCreateWindow('')
    model = Model3D('Obj\Cube.obj')
    print('Vertex:\n {}'.format(model.vertex))
    print('Faces:\n {}'.format(model.faces))
    print('Center:\n {}'.format(model.center))
    print('Radius:\n {}'.format(model.radius))
    print('Lines:\n {}'.format(model.lines))
    print('Modelview Matrix:\n {}'.format(np.round(model.getModelviewMatrix(),2)))
    print('Projection Matrix:\n {}'.format(np.round(model.getProjectionMatrix(),2)))
