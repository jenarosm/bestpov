from OpenGL.GL import*
from OpenGL.GLU import*
from OpenGL.GLUT import*
import numpy as np
from Model3D import Model3D
from Settings import*
from Profit import*

def project_vertex(v, m):
    v.append(1)
    projection = np.asarray(np.matmul(m,v)).reshape(-1)
    return projection/projection[3]

class Model2D():
    def __init__(self, model3, mp, mv):
        self.faces = model3.faces
        self.lines = model3.lines
        self.viewpoint = model3.viewpoint
        self.projection_matrix = np.matmul(mp,mv)
        self.vertex = np.asarray([ project_vertex(vertex, self.projection_matrix) for vertex in model3.vertex])
        self.profit = None

    def draw(self):
        reset_matrices()
        glMatrixMode(GL_PROJECTION)
        gluOrtho2D(-1,1,-1,1)
        glMatrixMode(GL_MODELVIEW)
        glColor4fv(LINE_COLOR)
        for line in self.lines:
            glBegin(GL_LINE_LOOP)
            glVertex2dv(self.vertex[line[0]-1][0:2])
            glVertex2dv(self.vertex[line[1]-1][0:2])
            glEnd()
        reset_matrices()

    def calculateProfit(self):
        self.top_view = isBetween(self.viewpoint[2],TOP_VIEW)
        self.area, self.ratio, self.front, self.back = total_area(self)
        self.vertex_repulsion = vertex_repulsion(self)
        self.tight_angles,self.parallel_repulsion,self.crossing_edges = edge_penalties(self)

        self.profit = self.area*self.ratio/(1+self.tight_angles+self.parallel_repulsion+self.crossing_edges+self.vertex_repulsion)*(self.top_view*TOP_VIEW_MULTIPLIER)
        return self.profit

if __name__=='__main__':
    glutInit(sys.argv)
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
    glutInitWindowSize(500, 500)
    WndId = glutCreateWindow('')
    model3 = Model3D('Obj\Cube.obj')
    mv = model3.getModelviewMatrix()
    mp = model3.getProjectionMatrix()
    model2 = Model2D(model3, mp, mv)
    print('Vertex:\n {}'.format(model2.vertex[:,:2]))
    print('Faces:\n {}'.format(model2.faces))
    print('Lines:\n {}'.format(model2.lines))
    print('Projection Matrix:\n {}'.format(model2.projection_matrix))
