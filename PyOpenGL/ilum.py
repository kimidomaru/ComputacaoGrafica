import OpenGL.GLUT as GLUT
import OpenGL.GLU as GLU
import OpenGL.GL as GL
from sys import argv
from math import sin, cos, pi, sqrt

# Variaveis Figura
vertices = 3
raio = 2
altura_prisma = 3
piramid_modif = 0.5

background_color = (0.2, 0.150, 0.150, 1)
count = 0

X = 0
Y = 1
Z = 2

materials = [   
    #Ouro
    [
        (0.24725,  0.1995,  0.0745,  1.0),
        (0.75164,  0.60648,  0.22648,  1.0),
        (0.628281,  0.555802,  0.366065,  1.0),
        (51.2)
    ],         
    #Prata
    [
        (0.19225,  0.19225,  0.19225,  1.0),
        (0.50754,  0.50754,  0.50754,  1.0),
        (0.508273,  0.508273,  0.508273,  1.0),
        (51.2)
    ],              
    #Bronze
    [
        (0.2125, 0.1275, 0.054, 1.0),
        (0.714, 0.4284, 0.18144, 1.0),
        (0.393548, 0.271906, 0.166721, 1.0),
        (25.6)
    ],
    #Cobre
    [
        (0.19125, 0.0735, 0.0225, 1.0),
        (0.7038, 0.27048, 0.0828, 1.0),
        (0.256777, 0.137622,  0.086014,  1.0),
        (12.8)
    ],           
    #Esmeralda
    [
        (0.0215,  0.1745,  0.0215,  0.55),
        (0.07568,  0.61424,  0.07568,  0.55),
        (0.633,  0.727811,  0.633,  0.55),
        (76.8)
    ],         
    #Jade
    [
        (0.135,  0.2225,  0.1575,  0.95),
        (0.54,  0.89,  0.63,  0.95),
        (0.316228,  0.316228,  0.316228,  0.95),
        (12.8)
    ],         
    #Obsidiana
    [
        (0.05375,  0.05,  0.06625,  0.82),
        (0.18275,  0.17,  0.22525,  0.82),
        (0.332741,  0.328634,  0.346435,  0.82),
        (38.4)
    ]         
]


# Functions
def normal_calculate(v0, v1, v2):
    U = (v2[X]-v0[X], v2[Y]-v0[Y], v2[Z]-v0[Z])
    V = (v1[X]-v0[X], v1[Y]-v0[Y], v1[Z]-v0[Z])
    NORMAL = ((U[Y]*V[Z]-U[Z]*V[Y]),(U[Z]*V[X]-U[X]*V[Z]),(U[X]*V[Y]-U[Y]*V[X]))
    normal_comprimento = sqrt(NORMAL[X]*NORMAL[X]+NORMAL[Y]*NORMAL[Y]+NORMAL[Z]*NORMAL[Z])
    return (NORMAL[X]/normal_comprimento, NORMAL[Y]/normal_comprimento, NORMAL[Z]/normal_comprimento)


def inverted_normal_calculate(v0, v1, v2):
    U = ( v2[X]-v0[X], v2[Y]-v0[Y], v2[Z]-v0[Z] )
    V = ( v1[X]-v0[X], v1[Y]-v0[Y], v1[Z]-v0[Z] )
    NORMAL = ( (U[Y]*V[Z]-U[Z]*V[Y]),(U[Z]*V[X]-U[X]*V[Z]),(U[X]*V[Y]-U[Y]*V[X]))
    normal_comprimento = sqrt(NORMAL[X]*NORMAL[X]+NORMAL[Y]*NORMAL[Y]+NORMAL[Z]*NORMAL[Z])
    return (-NORMAL[X]/normal_comprimento, -NORMAL[Y]/normal_comprimento, -NORMAL[Z]/normal_comprimento)


def figure():

    pontos_poligono = []
    angulo_face = (2*pi)/vertices
    
    GL.glPushMatrix()
    
    GL.glTranslatef(0.0, -1.0, 0.0)
    GL.glRotatef(-80,1.0,0.0,0.0)
  
  
    #FIGURA
    # Parte de baixo
    GL.glBegin(GL.GL_POLYGON)
    for i in range(vertices):
        x = raio * cos(i*angulo_face)
        y = raio * sin(i*angulo_face)
        pontos_poligono += [ (x,y) ]
        GL.glVertex3f(x,y,0.0)
    
    u = (pontos_poligono[0][0], pontos_poligono[0][1], 0)
    v = (pontos_poligono[1][0], pontos_poligono[1][1], 0)
    p = (pontos_poligono[2][0], pontos_poligono[2][1], 0)

    GL.glNormal3fv(inverted_normal_calculate(u,v,p))
    GL.glEnd()

    # Cima
    GL.glBegin(GL.GL_POLYGON)
    for x,y in pontos_poligono:
        GL.glVertex3f(piramid_modif*x,piramid_modif*y, altura_prisma)
    
    u = (pontos_poligono[0][0], pontos_poligono[0][1], altura_prisma)
    v = (pontos_poligono[1][0], pontos_poligono[1][1], altura_prisma)
    p = (pontos_poligono[2][0], pontos_poligono[2][1], altura_prisma)

    GL.glNormal3fv(normal_calculate(u,v,p))
    GL.glEnd()

    # Lados
    GL.glBegin(GL.GL_QUADS)
    for i in range(vertices):
        u = (pontos_poligono[i][0],pontos_poligono[i][1],0)
        v = (piramid_modif*pontos_poligono[i][0],piramid_modif*pontos_poligono[i][1],altura_prisma)
        p = (piramid_modif*pontos_poligono[(i+1)%vertices][0],piramid_modif*pontos_poligono[(i+1)%vertices][1],altura_prisma)
        q = (pontos_poligono[(i+1)%vertices][0],pontos_poligono[(i+1)%vertices][1],0)

        GL.glNormal3fv(normal_calculate(u,v,q))
        
        GL.glVertex3fv(u)
        GL.glVertex3fv(v)
        GL.glVertex3fv(p)
        GL.glVertex3fv(q)
    GL.glEnd()

    GL.glPopMatrix()


def draw():
    global count

    GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
    GL.glRotatef(2,1,3,0)

    if count % 150 == 0:
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, materials[(count+1)%len(materials)][0])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, materials[(count+1)%len(materials)][1])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materials[(count+1)%len(materials)][2])
        GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, materials[(count+1)%len(materials)][3])
    count += 1

    figure()

    GLUT.glutSwapBuffers()


def timer(i):
    GLUT.glutPostRedisplay()
    GLUT.glutTimerFunc(35, timer, 1)

def mouse_click(button, state, x, y):
    global piramid_modif, vertices

    #alterna entre piramide e prisma
    if button == GLUT.GLUT_MIDDLE_BUTTON and state == GLUT.GLUT_DOWN:
        if piramid_modif == 1:
            piramid_modif = 0.5
        else:
            piramid_modif = 1
    #aumenta o nº de vertices
    if button == GLUT.GLUT_LEFT_BUTTON and vertices <= 12:
        vertices += 1
    #diminui o nº de vertices
    elif button == GLUT.GLUT_RIGHT_BUTTON and vertices > 3:
        vertices -= 1

    GLUT.glutPostRedisplay()


def reshape(w,h):
    GL.glViewport(0,0,w,h)
    GL.glMatrixMode(GL.GL_PROJECTION)
    GLU.gluPerspective(45, float(w) / float(h), 0.1, 50.0)
    GL.glMatrixMode(GL.GL_MODELVIEW)
    GL.glLoadIdentity()

    GLU.gluLookAt(10,0,0,0,0,0,0,1,0)
    

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

    GLUT.glutCreateWindow("Iluminacao Prisma/Piramide")

    # Reshape 
    GLUT.glutReshapeFunc(reshape)

    # Desenha
    GLUT.glutDisplayFunc(draw)

    # Input
    GLUT.glutMouseFunc(mouse_click)
    
    GL.glShadeModel(GL.GL_SMOOTH)

    #First Material
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_AMBIENT, materials[0][0])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_DIFFUSE, materials[0][1])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_SPECULAR, materials[0][2])
    GL.glMaterialfv(GL.GL_FRONT, GL.GL_SHININESS, materials[0][3])

    posicaoLuz = (12,0,0)
    GL.glEnable(GL.GL_LIGHTING)
    GL.glEnable(GL.GL_LIGHT0)
    GL.glLightfv(GL.GL_LIGHT0, GL.GL_POSITION, posicaoLuz)

    GL.glEnable(GL.GL_MULTISAMPLE)
    GL.glEnable(GL.GL_DEPTH_TEST)

    GL.glClearColor(*background_color)

    # posicao da camera
    GLU.gluPerspective(-45, largura / altura, 0.1, 100.0)


    GLUT.glutTimerFunc(50, timer, 1)
    GLUT.glutMainLoop()


if(__name__ == '__main__'):
    main()