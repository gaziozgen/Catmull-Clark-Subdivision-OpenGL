# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from Vec3D import Vec3D
from Mat3D import Mat3D
from Object3D import Object3D
from ObjectReader import ObjectReader


class Scene:
    def __init__(self):
        self.shape = None
        self.rotate_x = 0
        self.rotate_y = 0
        self.show_vertices = True
        self.show_edges = True
        self.show_faces = True
        self.distance = -10

    def draw(self):

        self.user_information()  # UI

        self.shape.clear_stack()  # clear transform stack
        self.shape.stack.append(Mat3D.translation(0.0, 0.0, self.distance))  # distance in z
        self.shape.stack.append(Mat3D.rotate_on_x(self.rotate_y))  # rotate on x
        self.shape.stack.append(Mat3D.rotate_on_y(self.rotate_x))  # rotate on y

        self.shape.calculate_combined_matrix()
        if self.show_vertices:
            self.shape.draw_vertices()
        if self.show_edges:
            self.shape.draw_edges()
        if self.show_faces:
            self.shape.draw_faces()

    # printing UI
    def user_information(self):

        glColor3f(0.9, 0.9, 0.9)
        glWindowPos2i(5, 80)

        line = "Subdivision level: " + str(len(self.shape.old_face_states))
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
        glWindowPos2i(5, 65)

        line = "Hit + or - key to change subdivision."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
        glWindowPos2i(5, 50)

        line = "Hit 1, 2, 3 to change visibility of vertices edges and faces."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
        glWindowPos2i(5, 35)

        line = "Click and drag the left mouse button to rotate shape."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
        glWindowPos2i(5, 20)

        line = "Scroll for change distance."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))
        glWindowPos2i(5, 5)

        line = "Hit ESC key to quit."
        for i in line:
            glutBitmapCharacter(GLUT_BITMAP_HELVETICA_12, ord(i))


