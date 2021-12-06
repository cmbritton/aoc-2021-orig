class DataObj(object):
    def __init__(self):
        pass

    def to_string(self):
        return ''.format()


class PuzzleObj(object):

    def __init__(self):
        self.data = []

    def add_data(self, input_line):
        pass

    def print_part_1_result(self):
        pass

    def print_part_2_result(self):
        pass

    def to_string(self):
        result = ''.format()
        return result


def run_part_1():
    puzzle_obj = PuzzleObj()
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        while input_line:
            puzzle_obj.add_data(input_line)
            input_line = data_file.readline()
    puzzle_obj.print_part_1_result()


def run_part_2():
    puzzle_obj = PuzzleObj()
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        while input_line:
            puzzle_obj.add_data(input_line)
            input_line = data_file.readline()
    puzzle_obj.print_part_2_result()


def main():
    run_part_1()
    run_part_2()


main()
