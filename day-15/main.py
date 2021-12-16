import numpy as np


def right(point):
    if point is None:
        return None
    x, y = point
    if x < matrix.shape[1] - 1:
        return x + 1, y
    else:
        return None


def down(point):
    if point is None:
        return None
    x, y = point
    if y < matrix.shape[0] - 1:
        return x, y + 1
    else:
        return None


def left(point):
    return down(point)


def get_paths(start, finish, current_path, paths, depth=0):
    global total_paths
    depth += 1
    if start is None:
        total_paths += 1
        return
    current_path.append(start)
    # print('stack depth = {}'.format(depth))
    # print(current_path)
    # print_paths(paths)
    # print('')
    if start == finish:
        total_paths += 1
        paths.append(current_path.copy())
    else:
        get_paths(left(start), finish, current_path, paths, depth)
        get_paths(right(start), finish, current_path, paths, depth)
    current_path.pop()
    return paths


def print_paths(paths):
    for path in paths:
        for x, y in path:
            print(matrix[x][y], end='')
        print('')


def print_path(path):
    result = ''
    for x, y in path:
        result += str(matrix[x][y])
    return result


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

matrix = np.zeros((len(lines[0]), len(lines)), np.ubyte)

for y in range(len(lines)):
    for x in range(len(lines[0])):
        matrix[x][y] = lines[y][x]  # Transpose rows and columns, so we can use x,y coordinates

lowest_risk = None
lowest_risk_path = None

total_paths = 0

START_POINT = (0, 0)
END_POINT = (matrix.shape[1] - 1, matrix.shape[0] - 1)
for path in get_paths((0, 0), END_POINT, [], []):
    risk = 0
    for x, y in path:
        if (x, y) != START_POINT:
            risk += matrix[x][y]
    if lowest_risk is None or risk < lowest_risk:
        lowest_risk = risk
        lowest_risk_path = path
print('Part 1, lowest risk = {}, total paths = {}, path = {}'.format(lowest_risk, total_paths, print_path(
    lowest_risk_path)))
