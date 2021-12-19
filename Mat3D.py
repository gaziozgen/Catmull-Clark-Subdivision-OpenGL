# CENG 487 Assignment4 by
# Gazi Özgen
# StudentId: 250201051
# 12 2021

import numpy as np


class Mat3D:

    def __init__(self, array2d, operation=""):
        self.matrix = array2d
        self.operation = operation

    def multiply(self, mat3d):
        return Mat3D(np.matmul(mat3d.matrix, self.matrix))

    def add(self, mat3d):
        return Mat3D(np.add(self.matrix, mat3d.matrix))

    def transpose(self):
        return Mat3D(np.transpose(self.matrix))

    @staticmethod
    def multiplication(array1, array2):
        return Mat3D(np.matmul(array1, array2))

    @staticmethod
    def translation(x, y, z):
        mat3d = Mat3D([[1, 0, 0, x],
                       [0, 1, 0, y],
                       [0, 0, 1, z],
                       [0, 0, 0, 1]], "T")
        return mat3d

    @staticmethod
    def inv_translation(x, y, z):
        mat3d = Mat3D([[1, 0, 0, -x],
                       [0, 1, 0, -y],
                       [0, 0, 1, -z],
                       [0, 0, 0, 1]], "T")
        return mat3d

    @staticmethod
    def scale(x, y, z):
        mat3d = Mat3D([[x, 0, 0, 0],
                       [0, y, 0, 0],
                       [0, 0, z, 0],
                       [0, 0, 0, 1]], "S")
        return mat3d

    @staticmethod
    def inv_scale(x, y, z):
        mat3d = Mat3D([[1/x, 0, 0, 0],
                       [0, 1/y, 0, 0],
                       [0, 0, 1/z, 0],
                       [0, 0, 0, 1]], "S")
        return mat3d

    @staticmethod
    def rotate_on_x(radian):
        mat3d = Mat3D([[1, 0, 0, 0],
                       [0, np.cos(radian), -np.sin(radian), 0],
                       [0, np.sin(radian), np.cos(radian), 0],
                       [0, 0, 0, 1]], "R")
        return mat3d

    @staticmethod
    def inv_rotate_on_x(radian):
        mat3d = Mat3D([[1, 0, 0, 0],
                       [0, np.cos(radian), np.sin(radian), 0],
                       [0, -np.sin(radian), np.cos(radian), 0],
                       [0, 0, 0, 1]], "R")
        return mat3d

    @staticmethod
    def rotate_on_y(radian):
        mat3d = Mat3D([[np.cos(radian), 0, np.sin(radian), 0],
                       [0, 1, 0, 0],
                       [-np.sin(radian), 0, np.cos(radian), 0],
                       [0, 0, 0, 1]], "R")
        return mat3d

    @staticmethod
    def inv_rotate_on_y(radian):
        mat3d = Mat3D([[np.cos(radian), 0, -np.sin(radian), 0],
                       [0, 1, 0, 0],
                       [np.sin(radian), 0, np.cos(radian), 0],
                       [0, 0, 0, 1]], "R")
        return mat3d

    @staticmethod
    def rotate_on_z(radian):
        mat3d = Mat3D([[np.cos(radian), -np.sin(radian), 0, 0],
                       [np.sin(radian), np.cos(radian), 0,  0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], "R")
        return mat3d

    @staticmethod
    def inv_rotate_on_z(radian):
        mat3d = Mat3D([[np.cos(radian), np.sin(radian), 0, 0],
                       [-np.sin(radian), np.cos(radian), 0,  0],
                       [0, 0, 1, 0],
                       [0, 0, 0, 1]], "R")
        return mat3d
