# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

from CustomHalfEdge import Face
from CustomHalfEdge import Vertex
from CustomHalfEdge import Edge
from Mat3D import Mat3D
from Vec3D import Vec3D
from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np


class Object3D:

    def __init__(self):

        # transform stack
        self.stack = [Mat3D([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])]
        self.combined_matrix = None

        self.vertices = []      # list of vertices
        self.edges = []         # list of edges
        self.faces = []         # list of faces

        self.old_vertex_states = []     # old states of vertices
        self.old_edge_states = []       # old states of edges
        self.old_face_states = []       # old states of faces

    # calculate combined matrix for drawing operations
    def calculate_combined_matrix(self):
        # creating product matrix of transform stack
        product_matrix = Mat3D(self.stack[0].matrix)

        # multiply matrix values of stack end to begin
        for i in range(len(self.stack)):
            product_matrix = product_matrix.multiply(self.stack.pop())

        # Data form of product matrix
        self.combined_matrix = product_matrix

    # clears transformation stack
    def clear_stack(self):
        self.stack = [Mat3D([[1, 0, 0, 0],
                             [0, 1, 0, 0],
                             [0, 0, 1, 0],
                             [0, 0, 0, 1]])]

    # draws vertices of object
    def draw_vertices(self):
        glColor3f(0.9, 0.0, 0.0)

        # Data form of combined matrix
        final_matrix = self.combined_matrix.matrix

        glPointSize(5)
        glBegin(GL_POINTS)

        # multiply each value of vertices list with combined matrix and show
        for vertex in self.vertices:
            if vertex is not None:
                point = Mat3D.multiplication(final_matrix, vertex.vec3d.to_matrix()).matrix
                glVertex3f(point[0], point[1], point[2])

        glEnd()

    # draws edges of object
    def draw_edges(self):
        glColor3f(0.9, 0.7, 0.0)

        # Data form of combined matrix
        final_matrix = self.combined_matrix.matrix

        glLineWidth(2)

        # multiply end values of edges with combined matrix and show
        for edge in self.edges:
            glBegin(GL_LINES)

            point = Mat3D.multiplication(final_matrix, edge.origin.vec3d.to_matrix()).matrix
            glVertex3f(point[0], point[1], point[2])

            point = Mat3D.multiplication(final_matrix, edge.destination.vec3d.to_matrix()).matrix
            glVertex3f(point[0], point[1], point[2])

            glEnd()

    # draws faces of object
    def draw_faces(self):
        glColor3f(0.1, 0.4, 1.0)

        # Data form of combined matrix
        final_matrix = self.combined_matrix.matrix

        # draw each edge of each face by multiplying vertex values by combined matrix
        for face in self.faces:
            edge = face.edge

            glBegin(GL_QUADS)
            for i in range(4):
                edge = edge.front
                point = Mat3D.multiplication(final_matrix, edge.origin.vec3d.to_matrix()).matrix
                glVertex3f(point[0], point[1], point[2])

            glEnd()

    # subdivide with catmull-clark
    def subdivide(self):

        # create arrays for the next shape
        next_vertices = []
        next_edges = []
        next_faces = []

        # assign a mid point to each face
        for face in self.faces:
            face.create_mid_point()
            next_vertices.append(face.mid_point)

        # assign a edge point to the all edges
        for edge in self.edges:
            edge.create_product_point()
            next_vertices.append(edge.product_point)

        # calculate each original vertices new position
        for vertex in self.vertices:
            if vertex is not None:
                vertex.create_next_point()
                next_vertices.append(vertex.product_point)

        # for each face, switch to new vertices and apply same data structure
        for face in self.faces:
            edge = face.edge
            for i in range(4):
                sub_face = Face()

                # create new edges
                sub_edge1 = Edge(edge.origin.product_point, edge.product_point)
                sub_edge2 = Edge(edge.product_point, edge.face.mid_point)
                sub_edge3 = Edge(edge.face.mid_point, edge.back.product_point)
                sub_edge4 = Edge(edge.back.product_point, edge.origin.product_point)

                # append to the list
                next_edges.append(sub_edge1)
                next_edges.append(sub_edge2)
                next_edges.append(sub_edge3)
                next_edges.append(sub_edge4)

                # control and assign edge to each edge
                if sub_edge1.origin.edge is None:
                    sub_edge1.origin.edge = sub_edge1
                if sub_edge2.origin.edge is None:
                    sub_edge2.origin.edge = sub_edge2
                if sub_edge3.origin.edge is None:
                    sub_edge3.origin.edge = sub_edge3
                if sub_edge4.origin.edge is None:
                    sub_edge4.origin.edge = sub_edge4

                # assign fronts
                sub_edge1.front = sub_edge2
                sub_edge2.front = sub_edge3
                sub_edge3.front = sub_edge4
                sub_edge4.front = sub_edge1

                # assign backs
                sub_edge1.back = sub_edge4
                sub_edge2.back = sub_edge1
                sub_edge3.back = sub_edge2
                sub_edge4.back = sub_edge3

                # assign faces
                sub_edge1.face = sub_face
                sub_edge2.face = sub_face
                sub_edge3.face = sub_face
                sub_edge4.face = sub_face

                # update face and append to list
                sub_face.edge = sub_edge1
                next_faces.append(sub_face)

                # for next iteration
                edge = edge.front

        # find symmetric edges in next shape an assign them other's reference
        for i in range(len(next_edges)):
            if next_edges[i].symmetry is not None:
                continue
            for j in range(i + 1, len(next_edges)):
                if next_edges[i].is_symmetry_of(next_edges[j]):
                    next_edges[i].symmetry = next_edges[j]
                    next_edges[j].symmetry = next_edges[i]
                    break

        # switch lists and store old ones in old states lists
        self.old_vertex_states.append(self.vertices)
        self.old_edge_states.append(self.edges)
        self.old_face_states.append(self.faces)
        self.vertices = next_vertices
        self.edges = next_edges
        self.faces = next_faces

    # undo subdivide
    def undo_subdivide(self):
        if len(self.old_face_states) > 0:   # if there is a data

            # load lists back from old state lists
            self.vertices = self.old_vertex_states.pop()
            self.edges = self.old_edge_states.pop()
            self.faces = self.old_face_states.pop()
