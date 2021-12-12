import networkx as nx


# class Node(object):
#
#     def __init__(self, name):
#         self.name = name
#         self.incoming = []
#         self.outgoing = []
#
#     def is_small(self):
#         return self.name.islower()
#
#     def add_incoming(self, from_node):
#         if from_node not in self.incoming:
#             self.incoming.append(from_node)
#
#     def add_outgoing(self, to_node):
#         if to_node not in self.outgoing:
#             self.outgoing.append(to_node)
#
#     def __eq__(self, other):
#         return self.name == other
#
#     def __neg__(self, other):
#         return self.name != other
#
#     def __hash__(self):
#         return hash(self.name)
#
#     def to_string(self):
#         result = ''
#         if self.incoming:
#             result += '['
#             for n in self.incoming:
#                 result += n.name
#                 result += ', '
#             if result.endswith(', '):
#                 result = result[:-2]
#                 result += '] -> '
#         result = self.name
#         if self.outgoing:
#             result += ' -> ['
#             for n in self.outgoing:
#                 result += n.name
#                 result += ', '
#             if result.endswith(', '):
#                 result = result[:-2]
#                 result += ']'
#         return result


class Graph(object):

    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        self.nodes.add(node)
        if node not in self.edges:
            self.edges[node] = []

    def add_edge(self, from_node, to_node):
        self.add_node(from_node)
        self.add_node(to_node)
        self.edges[from_node].append(to_node)
        self.edges[to_node].append(from_node)

    def to_string(self):
        result = ''
        for node in self.nodes:
            result += node + ' -> ' + str(self.edges[node])
            result += '\n'
        return result

    def is_any_small_node_in_path_twice(self, path):
        nodes_in_path = []
        for node in path:
            if node.islower():
                if node in nodes_in_path:
                    return True
                else:
                    nodes_in_path.append(node)
        return False

    def can_add_small_node(self, node, path, is_part_2):
        if node == 'start' and node in path:
            return False
        if node.islower() and node in path:
            if not is_part_2:
                return False
            else:
                if self.is_any_small_node_in_path_twice(path):
                    return False
        return True

    def get_all_paths(self, start, end, path, is_part_2):
        global path_count, paths
        if not self.can_add_small_node(start, path, is_part_2):
            return
        path.append(start)
        if start == end:
            paths.append(path.copy())
        else:
            for child_node in g.edges[start]:
                if self.can_add_small_node(child_node, path, is_part_2) or child_node.isupper():
                    self.get_all_paths(child_node, end, path, is_part_2)
        path.pop()
        return path


g = Graph()
with open('data.txt', 'r') as data_file:
    lines = data_file.read().splitlines()
    for line in lines:
        from_node, to_node = line.split('-')
        g.add_edge(from_node, to_node)


paths = []
g.get_all_paths('start', 'end', [], False)
# for path in sorted(paths):
#     print(path)
print('Part 1, path_count = {}'.format(len(paths)))

paths = []
g.get_all_paths('start', 'end', [], True)
# for path in sorted(paths):
#     print(path)
print('Part 2, path_count = {}'.format(len(paths)))
