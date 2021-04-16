import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv
from math import sin, cos, pi

window = "Paraboloide de Revolucao"

background = (0.120, 0.200, 0.250, 1)

# Variaveis de rotacao
alpha = 90.0
beta = 45.0
delta_alpha = 0.7

# Figura
tam = 1.5
m, n = 20, 20
raio = 2

def funcao(i,j):
    t = ( (pi * i) / (m -1) ) - (pi / 2)
    p = 2*pi*j/(n-1)
    
    x = raio * cos(t) * cos(p)
    y = raio * sin(t)
    z = raio * cos(t) * sin(p)
    
    return x, y**2, z

def mesh():
    GL.glPushMatrix()
    #X
    GL.glRotatef(alpha, 0.0, 1.0, 0.0)
    #Y
    GL.glRotatef(beta, 0.0, 0.0, 1.0)

    # Figure
    for i in range(round(m/2)):
        GL.glBegin(GL.GL_QUAD_STRIP)

        for j in range(n):
            GL.glColor3fv(
                ((1.0*i/(m-1)),
                0.15,
                1 - (1.0*i/(m-1))))
            x, y, z = funcao(i,j)
            GL.glVertex3f(x,y,z)
            GL.glColor3fv(((1.0*(i+1)/(m-1)),
                             0.15,
                            1 - (1.0*(i+1)/(m-1))))
            x, y, z = funcao(i+1, j)
            GL.glVertex3f(x,y,z)
        GL.glEnd()

    GL.glPopMatrix()

def desenha():
    global alpha

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    mesh()
    alpha = alpha + delta_alpha

    GLUT.glutSwapBuffers()


def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(10, timer, 1)
 
GLUT.glutInit(argv)
GLUT.glutInitDisplayMode(
    GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE
)

screen_width = GLUT.glutGet(GLUT.GLUT_SCREEN_WIDTH)
screen_height = GLUT.glutGet(GLUT.GLUT_SCREEN_HEIGHT)

window_width = round(2 * screen_width / 3)
window_height = round(2 * screen_height / 3)

GLUT.glutInitWindowSize(window_width, window_height)
GLUT.glutInitWindowPosition(
    round((screen_width - window_width) / 2), round((screen_height - window_height) / 2)
)
GLUT.glutCreateWindow(window)

GLUT.glutDisplayFunc(desenha)

GL.glEnable(GL.GL_MULTISAMPLE)
GL.glEnable(GL.GL_DEPTH_TEST)

GL.glClearColor(*background)

GLU.gluPerspective(-45, window_width / window_height, 0.1, 100.0)
GL.glTranslatef(0.0, 0.0, -10)

GLUT.glutTimerFunc(10, timer, 1)
GLUT.glutMainLoop()
