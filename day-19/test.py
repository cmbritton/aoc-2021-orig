import unittest
from main import rotate_point
import numpy as np

point_data = [
    {'point': [1, 2, 3], 'rotation_factors': (0, 0, 0), 'expected_result': [1, 2, 3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 0, 1), 'expected_result': [-2, 1, 3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 0, 2), 'expected_result': [-1, -2, 3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 0, 3), 'expected_result': [2, -1, 3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 1, 0), 'expected_result': [3, 2, -1]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 2, 0), 'expected_result': [-1, 2, -3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 3, 0), 'expected_result': [-3, 2, 1]},
    {'point': [1, 2, 3], 'rotation_factors': (1, 0, 0), 'expected_result': [1, -3, 2]},
    {'point': [1, 2, 3], 'rotation_factors': (2, 0, 0), 'expected_result': [1, -2, -3]},
    {'point': [1, 2, 3], 'rotation_factors': (3, 0, 0), 'expected_result': [1, 3, -2]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 1, 1), 'expected_result': [-2, 3, -1]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 1, 2), 'expected_result': [-3, -2, -1]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 1, 3), 'expected_result': [2, -3, -1]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 2, 1), 'expected_result': [-2, -1, -3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 2, 2), 'expected_result': [1, -2, -3]},
    {'point': [1, 2, 3], 'rotation_factors': (0, 2, 3), 'expected_result': [2, 1, -3]},
]


class MyTestCase(unittest.TestCase):
    def test_rotation(self):
        for data in point_data:
            p = data['point']
            rf = data['rotation_factors']
            rp = rotate_point(p, rf).tolist()
            self.assertEqual(data['expected_result'], rp, 'test_rotation')


if __name__ == '__main__':
    unittest.main()
