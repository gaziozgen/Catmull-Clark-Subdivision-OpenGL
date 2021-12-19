# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

from CustomHalfEdge import Face
from CustomHalfEdge import Vertex
from CustomHalfEdge import Edge
from Vec3D import Vec3D
from Mat3D import Mat3D
from Object3D import Object3D


class ObjectReader:

    @staticmethod
    def read(file_name):
        new_object = Object3D()
        try:
            f = open(file_name)
            for line in f:

                # read vertices
                if line[:2] == "v ":
                    values = line.split()
                    vertex = (float(values[1]), float(values[2]), float(values[3]))
                    vertex = (round(vertex[0], 2), round(vertex[1], 2), round(vertex[2], 2))

                    # create Vertex object and add it to vertex list
                    vertex = Vertex(Vec3D(vertex[0], vertex[1], vertex[2], 1))
                    new_object.vertices.append(vertex)

                # read faces
                elif line[0] == "f":
                    values = line.split()
                    face_vertices = []
                    for i in range(1, len(values)):
                        face_vertices.append(int(values[i]) - 1)

                    # unique face
                    new_face = Face()
                    new_object.faces.append(new_face)

                    # first edge
                    first_new_edge = Edge(new_object.vertices[face_vertices[-1]],
                                          new_object.vertices[face_vertices[0]])
                    new_object.edges.append(first_new_edge)
                    first_new_edge.face = new_face

                    # control and assign edge to each edge
                    if new_object.vertices[face_vertices[-1]].edge is None:
                        new_object.vertices[face_vertices[-1]].edge = first_new_edge

                    new_face.edge = first_new_edge

                    # for next iterations in for loop
                    previous_edge = first_new_edge
                    new_edge = None

                    for i in range(len(face_vertices) - 1):

                        # creating new edge
                        new_edge = Edge(new_object.vertices[face_vertices[i]],
                                        new_object.vertices[face_vertices[i + 1]])

                        # assign references according to data structure
                        new_edge.face = new_face
                        new_object.edges.append(new_edge)

                        # control and assign edge to each edge
                        if new_object.vertices[face_vertices[i]].edge is None:
                            new_object.vertices[face_vertices[i]].edge = new_edge

                        # assign references according to data structure
                        previous_edge.front = new_edge
                        new_edge.back = previous_edge
                        previous_edge = new_edge

                    # assign references according to data structure
                    new_edge.front = first_new_edge
                    first_new_edge.back = new_edge

            # find symmetric edges in our shape an assign them other's reference
            for i in range(len(new_object.edges)):
                if new_object.edges[i].symmetry is not None:
                    continue
                for j in range(i+1, len(new_object.edges)):
                    if new_object.edges[i].is_symmetry_of(new_object.edges[j]):
                        new_object.edges[i].symmetry = new_object.edges[j]
                        new_object.edges[j].symmetry = new_object.edges[i]
                        break

            f.close()
            return new_object

        except IOError:
            print(".obj file not found.")
            return None
