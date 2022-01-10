import numpy as np
import itertools as it


class Rotation:
    AXIS_ROTATIONS = [
        (  # rotate 0 degrees around any axis
            (1, 0, 0),
            (0, 1, 0),
            (0, 0, 1)
        ),
        (  # rotate 90 degrees around x-axis
            (1, 0, 0),
            (0, 0, -1),
            (0, 1, 0)
        ),
        (  # rotate 180 degrees around x-axis
            (1, 0, 0),
            (0, -1, 0),
            (0, 0, -1)
        ),
        (  # rotate 270 degrees around x-axis
            (1, 0, 0),
            (0, 0, 1),
            (0, -1, 0)
        ),
        (  # rotate 90 degrees around y-axis
            (0, 0, 1),
            (0, 1, 0),
            (-1, 0, 0)
        ),
        (  # rotate 180 degrees around y-axis
            (-1, 0, 0),
            (0, 1, 0),
            (0, 0, -1)
        ),
        (  # rotate 270 degrees around y-axis
            (0, 0, -1),
            (0, 1, 0),
            (1, 0, 0)
        ),
        (  # rotate 90 degrees around z-axis
            (0, -1, 0),
            (1, 0, 0),
            (0, 0, 1)
        ),
        (  # rotate 180 degrees around z-axis
            (-1, 0, 0),
            (0, -1, 0),
            (0, 0, 1)
        ),
        (  # rotate 270 degrees around z-axis
            (0, 1, 0),
            (-1, 0, 0),
            (0, 0, 1)
        )
    ]

    rotation_matrices = []

    def __init__(self, rotation_matrix):
        self.rotation_matrix = rotation_matrix

    @classmethod
    def _init_rotation_matrices(cls):
        for i in range(len(cls.AXIS_ROTATIONS)):
            for j in range(len(cls.AXIS_ROTATIONS)):
                rotation_matrix = np.dot(cls.AXIS_ROTATIONS[i],
                                         cls.AXIS_ROTATIONS[j])
                cls._add_rotation_matrix(rotation_matrix)
        cls.rotation_matrices = np.array(cls.rotation_matrices,
                                         dtype=object)

    #
    # @classmethod
    # def _init_rotation_matrices(cls):
    #     cls.rotation_matrices = []
    #     for i, j in it.permutations(range(len(cls.AXIS_ROTATIONS)), r=2):
    #         rotation_matrix = np.dot(np.array(cls.AXIS_ROTATIONS[i],
    #                                           dtype=object),
    #                                  np.array(cls.AXIS_ROTATIONS[j],
    #                                           dtype=object))
    #         cls._add_rotation_matrix(rotation_matrix)
    #     cls.rotation_matrices = np.array(cls.rotation_matrices,
    #                                      dtype=object)

    @classmethod
    def _add_rotation_matrix(cls, rotation_matrix):
        for m in cls.rotation_matrices:
            if (m == rotation_matrix).all(axis=1).all():
                return
        cls.rotation_matrices.append(rotation_matrix)


print(f'len(Rotation.rotation_matrices) = {len(Rotation.rotation_matrices)}')
Rotation._init_rotation_matrices()
print(f'len(Rotation.rotation_matrices) = {len(Rotation.rotation_matrices)}')
