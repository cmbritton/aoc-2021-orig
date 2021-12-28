import unittest
from main import get_left_number_node, get_right_number_node, Tree, Node

test_get_left_number_data = [
    {'sfn': [[[[[9, 8], 1], 2], 3], 4], 'coord': [9, 8], 'expected_result': None},
    {'sfn': [[[[[9, 8], [7, 3]], 2], 3], 4], 'coord': [9, 8], 'expected_result': None},
    {'sfn': [7, [6, [5, [4, [3, 2]]]]], 'coord': [3, 2], 'expected_result': 4},
    {'sfn': [[6, [5, [4, [3, 2]]]], 1], 'coord': [3, 2], 'expected_result': 4},
    {'sfn': [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], 'coord': [7, 3], 'expected_result': 1},
]

test_get_right_number_data = [
    {'sfn': [[[[[9, 8], 1], 2], 3], 4], 'coord': [9, 8], 'expected_result': 1},
    {'sfn': [[[[[9, 8], [7, 3]], 2], 3], 4], 'coord': [9, 8], 'expected_result': 2},
    {'sfn': [7, [6, [5, [4, [3, 2]]]]], 'coord': [3, 2], 'expected_result': None},
    {'sfn': [[6, [5, [4, [3, 2]]]], 1], 'coord': [3, 2], 'expected_result': 1},
    {'sfn': [[3, [2, [1, [7, 3]]]], [6, [5, [4, [3, 2]]]]], 'coord': [7, 3], 'expected_result': 6}
]


class MyTestCase(unittest.TestCase):
    def test_get_left_number(self):
        for data in test_get_left_number_data:
            tree = Tree.from_list(data['sfn'])
            tree.print(tree.root)
            node = tree.find_node(tree.root, data['coord'])
            left_number_node = get_left_number_node(tree, tree.find_parent(tree.root, node))
            if data['expected_result']:
                self.assertEqual(data['expected_result'], left_number_node.value,
                                 f'Expected: {data["expected_result"]}\nActual: {left_number_node.value}')
            else:
                self.assertEqual(data['expected_result'], left_number_node,
                                 f'Expected: {data["expected_result"]}\nActual: {left_number_node}')

    def test_get_right_number(self):
        for data in test_get_right_number_data:
            tree = Tree.from_list(data['sfn'])
            print('\n\n')
            tree.print(tree.root)
            node = tree.find_node(tree.root, data['coord'])
            right_number_node = get_right_number_node(tree, tree.find_parent(tree.root, node))
            if data['expected_result']:
                self.assertEqual(data['expected_result'], right_number_node.value,
                                 f'Expected: {data["expected_result"]}\nActual: {right_number_node.value}')
            else:
                self.assertEqual(data['expected_result'], right_number_node,
                                 f'Expected: {data["expected_result"]}\nActual: {right_number_node}')


if __name__ == '__main__':
    unittest.main()
