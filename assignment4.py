# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
from Vec3D import Vec3D
from Mat3D import Mat3D
from Object3D import Object3D
from ObjectReader import ObjectReader
from Scene import Scene

# Number of the glut window.
window = 0

show_vertices = True
show_edges = True
show_faces = False
mouse_x = 0
mouse_y = 0
current_drag_x = 0
current_drag_y = 0
distance = -10        # distance between shape
scene = Scene()     # scene object

if len(sys.argv) == 2:
    new_object = ObjectReader.read(sys.argv[1])  # assign main shape to the scene read by the file
    if new_object is not None:
        scene.shape = new_object
    else:
        print("the .obj file entered in console is not exist. Assigned default cube")
        scene.shape = ObjectReader.read("default_cube.obj")
else:
    print("there is no .obj file entered in console. Assigned default cube")
    scene.shape = ObjectReader.read("default_cube.obj")


# A general OpenGL initialization function.  Sets all of the initial parameters.
def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
    glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
    glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
    glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
    glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
    glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()					# Reset The Projection Matrix

    #  Calculate The Aspect Ratio Of The Window
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


# The function called when our window is resized (which shouldn't happen if you enable fullscreen, below)
def ReSizeGLScene(Width, Height):
    if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small
        Height = 1

    glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)


# The main drawing function.
def DrawGLScene():

    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)	    # Clear The Screen And The Depth Buffer

    scene.show_vertices = show_vertices   # show vertices
    scene.show_edges = show_edges   # show edges
    scene.show_faces = show_faces  # show faces

    scene.distance = distance               # update distance on z
    scene.draw()                        # draw scene

    #  since this is double buffered, swap the buffers to display what just got drawn.
    glutSwapBuffers()


# The function called whenever a key is pressed. Note the use of Python tuples to pass in: (key, x, y)
def keyPressed(key, x, y):
    global show_vertices, show_edges, show_faces
    # If escape is pressed, kill everything.
    # ord() is needed to get the keycode

    if ord(key) == 27:
        # Escape key = 27
        glutLeaveMainLoop()
        return

    if ord(key) == 43:
        scene.shape.subdivide()          # subdivide selected shape

    elif ord(key) == 45:
        scene.shape.undo_subdivide()       # un subdivide selected shape

    if ord(key) == 49:
        show_vertices = not show_vertices

    if ord(key) == 50:
        show_edges = not show_edges

    if ord(key) == 51:
        show_faces = not show_faces


def scroll_check(*args):
    global distance

    if args[1] == 1:
        distance += 1
    elif args[1] == -1:
        distance -= 1

drag = False

def mouse_drag_check(*args):
    global mouse_x, mouse_y, drag, current_drag_x, current_drag_y

    drag = True

    scene.rotate_x = (args[0] - mouse_x) / 100 + current_drag_x
    scene.rotate_y = (args[1] - mouse_y) / 100 + current_drag_y

def update_mouse_pos(*args):
    global mouse_x, mouse_y, drag, current_drag_x, current_drag_y

    if drag:
        current_drag_x = scene.rotate_x
        current_drag_y = scene.rotate_y
    drag = False

    mouse_x = args[0]
    mouse_y = args[1]

def main():
    global window
    glutInit(sys.argv)

    # Select type of Display mode:
    #  Double buffer
    #  RGBA color
    #  Alpha components supported
    #  Depth buffer
    glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)

    # get a 640 x 480 window
    glutInitWindowSize(640, 480)

    # the window starts at the upper left corner of the screen
    glutInitWindowPosition(0, 0)

    # Okay, like the C version we retain the window id to use when closing, but for those of you new
    # to Python (like myself), remember this assignment would make the variable local and not global
    # if it weren't for the global declaration at the start of main.
    window = glutCreateWindow("CENG487 Development Env Test")

    # Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
    # set the function pointer and invoke a function to actually register the callback, otherwise it
    # would be very much like the C version of the code.
    glutDisplayFunc(DrawGLScene)

    # Uncomment this line to get full screen.
    # glutFullScreen()

    # When we are doing nothing, redraw the scene.
    glutIdleFunc(DrawGLScene)

    # Register the function called when our window is resized.
    glutReshapeFunc(ReSizeGLScene)

    # Register the function called when the keyboard is pressed.
    glutKeyboardFunc(keyPressed)
    glutMouseWheelFunc(scroll_check)

    glutMotionFunc(mouse_drag_check)
    glutPassiveMotionFunc(update_mouse_pos)
    #glutMouseFunc(mouse_drag_check)

    # Initialize our window.
    InitGL(640, 480)

    # Start Event Processing Engine
    glutMainLoop()

    # Print message to console, and kick off the main to get it rolling.
    print("Hit ESC key to quit.")
    print("Hit + or - key to change subdivision.")

main()

