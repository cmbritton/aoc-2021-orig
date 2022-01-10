import numpy as np


rotation_matrices = [
        np.array([  # rotate 0 degrees around any axis
            [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1]
        ]),
        np.array([  # rotate 90 degrees around x-axis
            [1, 0, 0],
            [0, 0, -1],
            [0, 1, 0]
        ]),
        np.array([  # rotate 180 degrees around x-axis
            [1, 0, 0],
            [0, -1, 0],
            [0, 0, -1]
        ]),
        np.array([  # rotate 270 degrees around x-axis
            [1, 0, 0],
            [0, 0, 1],
            [0, -1, 0]
        ]),
        np.array([  # rotate 90 degrees around y-axis
            [0, 0, 1],
            [0, 1, 0],
            [-1, 0, 0]
        ]),
        np.array([  # rotate 180 degrees around y-axis
            [-1, 0, 0],
            [0, 1, 0],
            [0, 0, -1]
        ]),
        np.array([  # rotate 270 degrees around y-axis
            [0, 0, -1],
            [0, 1, 0],
            [1, 0, 0]
        ]),
        np.array([  # rotate 90 degrees around z-axis
            [0, -1, 0],
            [1, 0, 0],
            [0, 0, 1]
        ]),
        np.array([  # rotate 180 degrees around z-axis
            [-1, 0, 0],
            [0, -1, 0],
            [0, 0, 1]
        ]),
        np.array([  # rotate 270 degrees around z-axis
            [0, 1, 0],
            [-1, 0, 0],
            [0, 0, 1]
        ])
    ]


results = []


def add_result(result):
    for a in results:
        if (a == result).all(axis=1).all():
            return False
    results.append(result)
    return True


for i in range(len(rotation_matrices)):
    for j in range(len(rotation_matrices)):
        result = np.dot(rotation_matrices[i], rotation_matrices[j])
        print('')
        if add_result(result):
            print('Added')
        else:
            print('Duplicate')
        for r in [0, 1, 2]:
            print('|', end='')
            for c in [0, 1, 2]:
                print(f' {rotation_matrices[i][r][c]:>2}', end='')
            print(' | |', end='')
            for c in [0, 1, 2]:
                print(f' {rotation_matrices[j][r][c]:>2}', end='')
            if r == 1:
                print(' | = |', end='')
            else:
                print(' |   |', end='')
            for c in [0, 1, 2]:
                print(f' {result[r][c]:>2}', end='')
            print(' |')

print(f'\nlen(results)={len(results)}')
