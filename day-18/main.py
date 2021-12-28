import re
from typing import Tuple
import time


class Tree(object):

    def __init__(self, root=None):
        self.root = root

    @staticmethod
    def from_list(sfn):
        tree = Tree(Tree._from_list(sfn))
        return tree

    @staticmethod
    def _from_list(sfn):
        node = Node(sfn, sfn[0], sfn[1])
        if type(sfn[0]) == list:
            node.left = Tree._from_list(sfn[0])
        elif type(sfn[0]) == int:
            node.left = Node(sfn[0])
        else:
            node.left = None

        if type(sfn[1]) == list:
            node.right = Tree._from_list(sfn[1])
        elif type(sfn[1]) == int:
            node.right = Node(sfn[1])
        else:
            node.right = None
        return node

    def find_node(self, node, value):
        if not node:
            return None
        if node.value == value:
            return node
        sub_node = self.find_node(node.left, value)
        if not sub_node:
            sub_node = self.find_node(node.right, value)
        return sub_node

    def path_to_root(self, node):
        path = []
        if node:
            path.append(node)
            sub_path = self.path_to_root(self.find_parent(self.root, node))
            if sub_path:
                path.extend(sub_path)
        return path

    def distance_to_root(self, node):
        return len(self.path_to_root(node))

    def find_parent(self, current_node, target_node):
        if not current_node:
            return None
        if current_node.left == target_node or current_node.right == target_node:
            return current_node
        node = self.find_parent(current_node.left, target_node)
        if not node:
            node = self.find_parent(current_node.right, target_node)
        return node

    def print(self, node, level=0):
        if node is not None:
            self.print(node.left, level + 1)
            print(' ' * 4 * level + '->', node.value)
            self.print(node.right, level + 1)

    def to_string(self, node):
        return str(self.as_list(node))

    def as_list(self, node):
        result = []
        if node is not None:
            if type(node.value) == list:
                result.append(self.as_list(node.left))
                result.append(self.as_list(node.right))
            else:
                return node.value
            return result
        return []


class Node(object):

    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


# def get_item(sfn, coordinates):
#     result = sfn
#     for i in range(len(coordinates)):
#         if type(result) == list:
#             result = result[coordinates[i]]
#         else:
#             return None
#     return result


# def depth(sfn):
#     return isinstance(sfn, list) and max(map(depth, sfn)) + 1


def get_left_number_node(tree, node):
    if node and node.left:
        if type(node.left.value) == int:
            return node.left
        else:
            return get_left_number_node(tree, tree.find_parent(tree.root, node))
    return None


def get_right_descend_right(node):
    if node and node.right:
        if type(node.right.value) == int:
            return node.right
        elif type(node.left.value) == int:
            return node.left
        else:
            return get_right_descend_right(node.right)
    return None


def get_right_number_node(tree, node):
    # if node == tree.root:
    #     return get_right_descend_right(node)
    if node and node.right:
        if type(node.right.value) == int:
            return node.right
        else:
            return get_right_number_node(tree, tree.find_parent(tree.root, node))
    return None


def explode(tree, node):
    left_number_node = get_left_number_node(tree, tree.find_parent(tree.root, node))
    if left_number_node and left_number_node.value:
        left_number_node.value += node.left.value
    right_number_node = get_right_number_node(tree, tree.find_parent(tree.root, node))
    if right_number_node and right_number_node.value:
        right_number_node.value += node.right.value
    node.value = 0
    node.left = node.right = None
    print(f'list = {tree.as_list(tree.root)}')


def scan_for_explodes(tree, node):
    if type(node.value) == list:
        if tree.distance_to_root(node) > 4:
            explode(tree, node)
        else:
            scan_for_explodes(tree, node.left)
            scan_for_explodes(tree, node.right)


def scan_for_splits(tree, node):
    pass


def reduce(tree):
    print(f'list = {tree.as_list(tree.root)}')
    scan_for_explodes(tree, tree.root)
    scan_for_splits(tree, tree.root)


def do_run(sfn):
    tree = Tree.from_list(sfn)
    # tree.print(tree.root)
    # print(f'list = {tree.as_list(tree.root)}')
    # print(f'str = {tree.to_string(tree.root)}')
    # print(f'tree = {tree.to_string(tree.root)}')
    reduce(tree)


def elapsed_time(start_time: int, end_time: int) -> str:
    t = end_time - start_time
    unit = 'seconds'
    if t < 1:
        t = t * 1000
        unit = 'milliseconds'
    if t < 1:
        t = t * 1000
        unit = 'microseconds'
    if t < 1:
        t = t * 1000
        unit = 'nanoseconds'

    return f'{t:.2f} {unit}'


def init_data():
    # with open('data.txt', 'r') as data_file:
    #     line = data_file.readline()
    # return list([[[[[9, 8], 1], 2], 3], 4])
    # return list([7, [6, [5, [4, [3, 2]]]]])
    # return list([[6, [5, [4, [3, 2]]]], 1])
    return list([[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]])


def main() -> None:
    sfn = init_data()

    start_time = time.perf_counter()
    do_run(sfn)
    end_time = time.perf_counter()
    print(f'\nPart 1, sfn: {sfn}')
    # print(f'Part 2, Total valid paths = {len(valid_paths)}')
    print(f'Elapsed time: {elapsed_time(start_time, end_time)}')


if __name__ == '__main__':
    main()
