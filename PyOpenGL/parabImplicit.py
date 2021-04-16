import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv

window = "Paraboloide Eq. Implicita"

background = (0.120, 0.200, 0.250, 1)

# Variaveis de rotacao
alpha = 90.0
beta = 45.0
delta_alpha = 0.7

# Figura
tam = 1.5
m, n = 80, 80
x0, y0 = -tam, -tam
xf, yf = tam, tam
dx, dy = (xf - x0)/m, (yf - y0)/n

def funcao(x,y):
    return x**2-y**2

def mesh():
    GL.glPushMatrix()
    GL.glTranslatef(0, 0, 0)

    # Rotacao
    #X
    GL.glRotatef(alpha, 0.0, 1.0, 0.0)
    #Y
    GL.glRotatef(beta, 0.0, 0.0, 1.0)

    # Figura
    for i in range(0, n):
        y = y0 + i*dy      
        GL.glColor3f(1-(i/n), 0.6, i/n)
        GL.glBegin(GL.GL_QUAD_STRIP)
        for j in range(0,m):
            x = x0 + j*dx
            GL.glVertex3f(x, y, funcao(x,y))
            GL.glVertex3f(x, y+dy, funcao(x, y+dy))
            
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
