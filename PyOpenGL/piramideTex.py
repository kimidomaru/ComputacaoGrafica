import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from png import Reader
from sys import argv
from math import sin, cos, pi

# Variaveis Figura
vertices = 3
raio = 2
altura_prisma = 3
piramid_modif = 0.5

# Rotation
left_button = False
alpha = 90.0
beta = 0
delta_alpha = 0.5

# Translation
right_button = False
delta_x, delta_y, delta_z = 0, 0, 0

down_x, down_y = 0, 0

background_color = (0.2, 0.150, 0.150, 1)

texture = []

def load_textures():
    global texture
    texture = GL.glGenTextures(2)

    png_img = Reader(filename='.\\texPiramide.png')

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
    

    pontos_poligono = []
    angulo_face = (2*pi)/vertices
    
    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)    
    GL.glLoadIdentity()    
    
    GL.glPushMatrix()
    
    GL.glTranslatef(0.0, 1.5, -10)
    GL.glRotatef(90,1.0,0.0,0.0)

    GL.glTranslatef(delta_x, delta_y, delta_z)

    # X 
    GL.glRotatef(alpha, 0.0, 0.0, 1.0)
    # Y 
    GL.glRotatef(beta, 0.0, 1.0, 0.0)

    # Figure
    GL.glBindTexture(GL.GL_TEXTURE_2D, texture[0])

    # Cima
    GL.glBegin(GL.GL_POLYGON)
    for x,y in pontos_poligono:
        GL.glTexCoord2f(x, y); GL.glVertex3f(piramid_modif*x,piramid_modif*y, altura_prisma)
    GL.glEnd()

    # Baixo
    GL.glBegin(GL.GL_POLYGON)
    for i in range(vertices):
        x = raio * cos(i*angulo_face)
        y = raio * sin(i*angulo_face)
        pontos_poligono += [ (x,y) ]
        GL.glTexCoord2f(x, y); GL.glVertex3f(x,y,0.0)
    GL.glEnd()


    # Lados
    GL.glBegin(GL.GL_QUADS)
    for i in range(vertices):
        GL.glTexCoord2f(0.0, 0.0); GL.glVertex3f(pontos_poligono[i][0],pontos_poligono[i][1],0)
        GL.glTexCoord2f(0.0, 1.0); GL.glVertex3f(piramid_modif*pontos_poligono[i][0],piramid_modif*pontos_poligono[i][1],altura_prisma)

        GL.glTexCoord2f(1.0, 1.0); GL.glVertex3f(piramid_modif*pontos_poligono[(i+1)%vertices][0],piramid_modif*pontos_poligono[(i+1)%vertices][1],altura_prisma)
        GL.glTexCoord2f(1.0, 0.0); GL.glVertex3f(pontos_poligono[(i+1)%vertices][0],pontos_poligono[(i+1)%vertices][1],0)
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
    global downX, downY, left_button, right_button, piramid_modif

    downX, downY = x, y

    left_button = button == GLUT.GLUT_LEFT_BUTTON and state == GLUT.GLUT_DOWN
    right_button = button == GLUT.GLUT_RIGHT_BUTTON and state == GLUT.GLUT_DOWN
    
    #alterna entre piramide e prisma
    if button == GLUT.GLUT_MIDDLE_BUTTON and state == GLUT.GLUT_DOWN:
        if piramid_modif == 1:
            piramid_modif = 0.5
        else:
            piramid_modif = 1


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

    largura = 1024
    altura = 768

    # get a 1024 x 768 window 
    GLUT.glutInitWindowSize(largura, altura)
    
    # the window starts at the upper left corner of the screen 
    GLUT.glutInitWindowPosition(0, 0)

    GLUT.glutCreateWindow("Piramide texturizada")

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