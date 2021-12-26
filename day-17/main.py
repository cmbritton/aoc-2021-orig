import re
from typing import Tuple
import time


# def reverse_step(x, y) -> Tuple[int, int]:

def plot_reverse_trajectory(trench_x, trench_y, min_x, max_x, min_y, max_y) -> list:
    trajectory = []
    x = trench_x
    y = trench_y
    while x > 0:
        x, y = reverse_step(x, y)
        if x == 0 and y == 0:
            return trajectory.reverse()
        if x < 0:
            return None
        trajectory.append((x, y))


def possible_x_values(x):
    x_values = [x]
    reverse_delta = 1
    while x >= 0:
        if x == 0:
            x_values.reverse()
            return x_values
        else:
            x -= reverse_delta
            x_values.append(x)
            reverse_delta += 1
    return []


def do_run(min_x, max_x, min_y, max_y) -> Tuple[int, int]:
    for trench_x in range(min_x, max_x + 1):
        for trench_y in range(min_y, max_y + 1):
            pass
            # start_x, start_y = plot_reverse_trajectory(trench_x, trench_y, min_x, max_x, min_y, max_y)
        x_values = possible_x_values(trench_x)
        print(f'x_values = {str(x_values)}')
    return 1, 1


def init_data() -> Tuple[int, int, int, int]:
    with open('data.txt', 'r') as data_file:
        line = data_file.readline()
    m = re.search(r'target area: x=([-0-9]*)\.\.([-0-9]*), y=([-0-9]*)\.\.([-0-9]*)', line)
    return int(m.group(1)), int(m.group(2)), int(m.group(3)), int(m.group(4))


def main() -> None:
    min_x, max_x, min_y, max_y = init_data()

    start_time = time.perf_counter()
    x, y = do_run(min_x, max_x, min_y, max_y)
    end_time = time.perf_counter()
    print(f'Part 1, init velocity = {(x, y)}')
    # print(f'Part 2, value = {value}')
    # print(f'Elapsed time: {elapsed_time(start_time, end_time)}')


if __name__ == '__main__':
    main()
