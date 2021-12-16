import numpy as np


def left(point):
    if point is None:
        return None
    x, y = point
    if x > 0:
        return x - 1, y
    else:
        return None


def right(point):
    if point is None:
        return None
    x, y = point
    if x < risk_level.shape[1] - 1:
        return x + 1, y
    else:
        return None


def up(point):
    if point is None:
        return None
    x, y = point
    if y > 0:
        return x, y - 1
    else:
        return None


def down(point):
    if point is None:
        return None
    x, y = point
    if y < risk_level.shape[0] - 1:
        return x, y + 1
    else:
        return None


def print_paths(paths):
    for path in paths:
        for x, y in path:
            print(risk_level[x][y], end='')
        print('')


def min_cost_index():
    lowest_cost = INFINITY
    lowest_cost_index = None
    for y in range(risk_level.shape[0]):
        for x in range(risk_level.shape[1]):
            if not visited[x][y] and accumulated_risk_level[x][y] < lowest_cost:
                lowest_cost = accumulated_risk_level[x][y]
                lowest_cost_index = (x, y)
    return lowest_cost_index


def get_unvisited_neighbors(point) -> list:
    unvisited_neighbors = []
    for neighbor in [left(point), right(point), up(point), down(point)]:
        if neighbor and not visited[neighbor]:
            unvisited_neighbors.append(neighbor)
    return unvisited_neighbors


with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

risk_level = np.zeros((len(lines[0]), len(lines)), np.ubyte)

for y in range(len(lines)):
    for x in range(len(lines[0])):
        risk_level[x][y] = lines[y][x]  # Transpose rows and columns, so we can use x,y coordinates

visited = np.zeros(risk_level.shape, dtype=bool)
# prev = np.zeros(risk_level.shape, dtype=object)
paths = []

START_POINT = (0, 0)
INFINITY = 2 ** 64
accumulated_risk_level = np.zeros(risk_level.shape, dtype=int)
accumulated_risk_level = accumulated_risk_level + INFINITY
accumulated_risk_level[START_POINT] = 0

END_POINT = (risk_level.shape[1] - 1, risk_level.shape[0] - 1)
while np.count_nonzero(visited) < visited.size:
    current_node = min_cost_index()
    visited[current_node] = True
    unvisited_neighbors = get_unvisited_neighbors(current_node)

    path = []
    for neighbor in unvisited_neighbors:
        neighbor_risk_level = accumulated_risk_level[current_node] + risk_level[neighbor]
        if neighbor_risk_level < accumulated_risk_level[neighbor]:
            accumulated_risk_level[neighbor] = neighbor_risk_level
            path.append(current_node)
            # prev[neighbor] = current_node
    paths.append(path)
    if current_node == END_POINT or accumulated_risk_level[current_node] == INFINITY or visited[END_POINT]:
        break
print('Part 1, lowest distance = {}'.format(accumulated_risk_level[END_POINT]))
