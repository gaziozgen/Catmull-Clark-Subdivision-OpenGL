# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

from Vec3D import Vec3D

# My data structure is very close to the half edge
# when use "front" I mean next to the counter clockwise direction, opposite for "back"
# edges stores; origin, destination, front, back, face, symmetry and product point for next subdivision
# faces stores; edge and mid point for next subdivision
# vertices stores; vector3d, edge and product point for next subdivision


class Edge:
    def __init__(self, origin, destination):
        self.origin = origin
        self.destination = destination

        self.symmetry = None
        self.front = None
        self.back = None
        self.face = None

        # for subdivision
        self.product_point = None   # average of adjacent face and edge points

    # compares vertices with other edge for checking symmetry
    def is_symmetry_of(self, other_edge):
        if other_edge.origin == self.destination and other_edge.destination == self.origin:
            return True
        else:
            return False

    # compares vertices with other edge for checking equality
    def is_equal(self, other_edge):
        if other_edge.origin == self.origin and other_edge.destination == self.destination:
            return True
        else:
            return False

    # use edge points and face points to create new edge point for subdivision
    def create_product_point(self):
        if self.product_point is None:
            total = Vec3D(0, 0, 0, 1)
            total.add_vector3d(self.origin.vec3d)
            total.add_vector3d(self.destination.vec3d)
            total.add_vector3d(self.face.mid_point.vec3d)
            total.add_vector3d(self.symmetry.face.mid_point.vec3d)
            product = Vertex(total.scalar_multiplication(1 / 4))
            self.product_point = product
            self.symmetry.product_point = product


class Vertex:

    def __init__(self, vec3d):
        self.vec3d = vec3d
        self.edge = None

        # for subdivision
        self.product_point = None   # weighted average of face and middle of original edge points

    # weighted average of face and middle of original edge points for subdivision
    def create_next_point(self):
        if self.edge is not None:
            n = 0
            start_edge = self.edge
            edge = start_edge

            total = Vec3D(0, 0, 0, 1)
            while True:
                total.add_vector3d(edge.origin.vec3d)
                total.add_vector3d(edge.destination.vec3d)
                total.add_vector3d(edge.face.mid_point.vec3d)

                n += 1
                edge = edge.symmetry.front
                if edge == start_edge:
                    break

            total.scalar_multiplication(1 / n)
            second_part = Vec3D.multiply_vector_with_value(self.vec3d, n - 3)
            total.add_vector3d(second_part)
            total.scalar_multiplication(1 / n)
            self.product_point = Vertex(total)


class Face:

    def __init__(self):
        self.edge = None
        self.mid_point = None   # average of 4 face points

    # average of 4 face points for subdivision
    def create_mid_point(self):
        total = Vec3D(0, 0, 0, 1)
        edge = self.edge
        for i in range(4):
            total.add_vector3d(edge.origin.vec3d)
            edge = edge.front
        self.mid_point = Vertex(total.scalar_multiplication(1/4))
