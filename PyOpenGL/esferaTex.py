import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from png import Reader
from sys import argv
from math import sin, cos, pi


# Variaveis da Esfera
n = 30
m = 30
radius = 2


#Funcao da esfera
def f(i,j):
    theta = ( (pi * i) / (n -1) ) - (pi / 2)
    phi = 2*pi*j/(m-1)
    
    x = radius * cos(theta) * cos(phi)
    y = radius * sin(theta)
    z = radius * cos(theta) * sin(phi)
    
    s = s_func(phi)

    t = t_func(theta)
    
    return x,y,z,s,t

def s_func(phi):
    return (phi/(2*pi))

def t_func(theta):
    return ((theta + (pi/2))/pi)

# Rotation
left_button = False
alpha = 90.0
beta = 0
delta_alpha = 0.5

# Translation
right_button = False
delta_x, delta_y= 0, 0

downX, downY = 0, 0

background_color = (0.2, 0.150, 0.150, 1)

texture = []

def load_textures():
    global texture
    texture = GL.glGenTextures(2)

    png_img = Reader(filename='.\mapa.png')

    w, h, pixels, metadata = png_img.read_flat()

    if(metadata['alpha']):
        modo = GL.GL_RGBA
    else:
        modo = GL.GL_RGB

    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    GL.glPixelStorei(GL.GL_UNPACK_ALIGNMENT, 1)
    GL.glTexImage2D(GL.GL_TEXTURE_2D, 0, modo, w, h, 0, modo, GL.GL_UNSIGNED_BYTE, pixels.tolist())
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_S, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_WRAP_T, GL.GL_REPEAT)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MAG_FILTER, GL.GL_NEAREST)
    GL.glTexParameterf(GL.GL_TEXTURE_2D, GL.GL_TEXTURE_MIN_FILTER, GL.GL_NEAREST)
    GL.glTexEnvf(GL.GL_TEXTURE_ENV, GL.GL_TEXTURE_ENV_MODE, GL.GL_DECAL)


def figure():
    
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)    
    GL.glLoadIdentity()    
    
    GL.glPushMatrix()

    GL.glTranslatef(delta_x, delta_y, 0)

    #X 
    GL.glRotatef(alpha, 0.0, 1.0, 0.0)
    #Y 
    GL.glRotatef(beta, 0.0, 0.0, 1.0)

    # Figure
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])
    for i in range(n):
        GL.glBegin(GL.GL_QUAD_STRIP)
        for j in range(m):
            
            x, y, z, s, t = f(i,j)
            GL.glTexCoord2f(s, t)
            GL.glVertex3f(x,y,z)


            x, y, z, s, t = f(i+1, j)
            GL.glTexCoord2f(s, t)
            GL.glVertex3f(x,y,z)
        GL.glEnd()

    GL.glPopMatrix()

    GLUT.glutSwapBuffers()


def draw():
    global alpha, left_button, right_button
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

    figure()
    #Rotacao Automatica
    alpha = alpha + delta_alpha
    GLUT.glutSwapBuffers()

def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(12, timer, 1)


def mouse_click(button, state, x, y):
    global downX, downY, left_button, right_button

    downX, downY = x, y

    left_button = button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN
    right_button = button == GLUT.GLUT_RIGHT_BUTTON and state == GLUT.GLUT_DOWN


def mouse_move(x, y):
    global alpha, beta, downX, downY, delta_x, delta_y, delta_alpha

    # Rotate
    if left_button:
        delta_alpha = 0
        # Alpha 
        alpha += ((x - downX) / 4.0) * -1
        if alpha >= 360:
            alpha -= 360
        if alpha <= 0:
            alpha += 360

        # Beta
        if alpha >= 180:
            beta -= (y - downY) / 4.0 * -1
        else:
            beta += (y - downY) / 4.0 * -1

        if beta >= 360:
            beta -= 360
        if beta <= 0:
            beta += 360

    # Translate
    if right_button:
        delta_x += -1 * (x - downX) / 100.0
        delta_y += (y - downY) / 100.0

    downX, downY = x, y

    GLUT.glutPostRedisplay()

def main():    
    GLUT.glutInit(argv)
    GLUT.glutInitDisplayMode(
        GLUT.GLUT_DOUBLE | GLUT.GLUT_RGBA | GLUT.GLUT_DEPTH | GLUT.GLUT_MULTISAMPLE
    )

    largura = 640
    altura = 480

    # get a 640 x 480 window 
    GLUT.glutInitWindowSize(largura, altura)
    
    # the window starts at the upper left corner of the screen 
    GLUT.glutInitWindowPosition(0, 0)

    GLUT.glutCreateWindow("Globo Terrestre")

    GLUT.glutDisplayFunc(draw)

    # Input
    GLUT.glutMouseFunc(mouse_click)
    GLUT.glutMotionFunc(mouse_move)

    load_textures()

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)
    GL.glEnable(GL.GL_TEXTURE_2D)

    GL.glClearColor(*background_color)
    GL.glClearDepth(1.0)
    GL.glDepthFunc(GL.GL_LESS)

    GL.glShadeModel(GL.GL_SMOOTH)
    GL.glMatrixMode(GL.GL_PROJECTION)

    # posicao da camera
    GLU.gluPerspective(-45, largura / altura, 0.1, 100.0)
    GL.glTranslatef(0.0, 0.0, -10)

    GL.glMatrixMode(GL.GL_MODELVIEW)

    GLUT.glutTimerFunc(10, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()