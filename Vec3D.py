# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

import numpy as np


class Vec3D:

    def __init__(self, x, y, z, w):
        self.values = [x, y, z, w]

    # convert vector to 2D matrix format
    def to_matrix(self):
        return [[self.values[0]], [self.values[1]], [self.values[2]], [self.values[3]]]

    # dot product with other vector3d
    def dot_product(self, other_vector3d):
        other_vector_values = other_vector3d.values
        product = 0
        for i in range(3):
            product += self.values[i] * other_vector_values[i]
        return product

    # cross product with other vector3d
    def cross_product(self, other_vector3d):
        values1 = self.values
        values2 = other_vector3d.values
        return Vec3D(values1[1]*values2[2] - values1[2]*values2[1],
                     values1[2]*values2[0] - values1[0]*values2[2],
                     values1[0]*values2[1] - values1[1]*values2[0], 0)

    # returns middle point between this vector3d and other vector3d
    def middle_point_with(self, other_vector3d):
        return Vec3D((self.values[0] + other_vector3d.values[0])/2,
                     (self.values[1] + other_vector3d.values[1])/2,
                     (self.values[2] + other_vector3d.values[2])/2, 1)

    # scalar value, length
    def magnitude(self):
        return np.sqrt(self.dot_product(self))

    # returns angle between this vector3d and other vector3d
    def angle_between_vectors(self, other_vector3d):
        value = self.dot_product(other_vector3d) / (self.magnitude() * other_vector3d.magnitude())
        return np.arccos(value)

    # returns projection vector to basis vector
    def projection_to_basis_vector(self, other_vector3d):
        values_b = other_vector3d.values

        multiply_value = self.magnitude() * np.cos(self.angle_between_vectors(other_vector3d)) / other_vector3d.magnitude()
        return Vec3D(values_b[0] * multiply_value,
                     values_b[1] * multiply_value,
                     values_b[2] * multiply_value, 0)

    # vector3 addition
    def add_vector3d(self, other_vector3d):
        for i in range(3):
            self.values[i] = self.values[i] + other_vector3d.values[i]

    # multiplying vector values with scalar value
    def scalar_multiplication(self, value):
        my_values = self.values
        for i in range(3):
            my_values[i] *= value
        return self

    # vector3 total
    @staticmethod
    def total(self, vector3d_1, vector3d_2):
        total = Vec3D(0, 0, 0, 1)
        for i in range(3):
            total.values[i] = vector3d_1.values[i] + vector3d_2.values[i]
        return total

    # multiplication
    @staticmethod
    def multiply_vector_with_value(vector3d, value):
        product = Vec3D(vector3d.values[0], vector3d.values[1], vector3d.values[2], 1)
        for i in range(3):
            product.values[i] *= value
        return product