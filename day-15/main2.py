import datetime

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


def get_unvisited_lowest_cost_nodes():
    global visited, accumulated_risk_level
    indexes = np.where(accumulated_risk_level == np.min(np.ma.masked_where(visited, accumulated_risk_level)))
    lowest_cost_points = []
    for i in range(len(indexes[0])):
        lowest_cost_points.append((indexes[0][i], indexes[1][i]))
    return lowest_cost_points


def get_unvisited_neighbors(point) -> list:
    unvisited_neighbors = []
    for neighbor in [left(point), right(point), up(point), down(point)]:
        if neighbor and not visited[neighbor]:
            unvisited_neighbors.append(neighbor)
    return unvisited_neighbors


def calculate_lowest_risk():
    while np.count_nonzero(visited) < visited.size:
        lowest_cost_points = get_unvisited_lowest_cost_nodes()
        for current_node in lowest_cost_points:
            visited[current_node] = True
            unvisited_neighbors = get_unvisited_neighbors(current_node)

            path = []
            if current_node == END_POINT:
                break
            for neighbor in unvisited_neighbors:
                neighbor_risk_level = accumulated_risk_level[current_node] + risk_level[neighbor]
                if neighbor_risk_level < accumulated_risk_level[neighbor]:
                    accumulated_risk_level[neighbor] = neighbor_risk_level
                    path.append(current_node)
            shortest_path.append(path)
            if current_node == END_POINT or accumulated_risk_level[current_node] == INFINITY or visited[END_POINT]:
                break


def expand_risk_level_along_axis(src_risk_level, axis_str, factor):
    axis = 1 if axis_str == 'x' else 0
    expansion_list = [src_risk_level]
    for i in range(factor - 1):
        tmp_expanded_risk_level = np.copy(src_risk_level)
        tmp_expanded_risk_level += 1 + i
        tmp_expanded_risk_level[tmp_expanded_risk_level > 9] = tmp_expanded_risk_level[tmp_expanded_risk_level > 9] % 9
        expansion_list.append(tmp_expanded_risk_level)
    return np.concatenate(tuple(expansion_list), axis=axis)


def expand_risk_level():
    expand_factor_x = expand_factor_y = 5
    expanded_risk_level = expand_risk_level_along_axis(risk_level, 'x', expand_factor_x)
    return expand_risk_level_along_axis(expanded_risk_level, 'y', expand_factor_y)


def reset_aux_vars():
    global shortest_path, visited, accumulated_risk_level, END_POINT

    paths = []
    visited = np.zeros(risk_level.shape, dtype=bool)
    accumulated_risk_level = np.zeros(risk_level.shape, dtype=int)
    accumulated_risk_level = accumulated_risk_level + INFINITY
    accumulated_risk_level[START_POINT] = 0
    END_POINT = (risk_level.shape[1] - 1, risk_level.shape[0] - 1)


print('Start: {}'.format(datetime.datetime.now()))

with open('data2.txt', 'r') as data_file:
    lines = data_file.read().splitlines()

risk_level = np.zeros((len(lines[0]), len(lines)), np.ubyte)

for y in range(len(lines)):
    for x in range(len(lines[0])):
        risk_level[x][y] = lines[y][x]  # Transpose rows and columns, so we can use x,y coordinates

visited = None
shortest_path = []

START_POINT = (0, 0)
END_POINT = None
INFINITY = 2 ** 32

accumulated_risk_level = None

reset_aux_vars()
calculate_lowest_risk()
print('Part 1, lowest distance = {}'.format(accumulated_risk_level[END_POINT]))

print(datetime.datetime.now())

risk_level = expand_risk_level()

reset_aux_vars()
calculate_lowest_risk()
print('Part 2, lowest distance = {}'.format(accumulated_risk_level[END_POINT]))
print(datetime.datetime.now())
print_paths(shortest_path)