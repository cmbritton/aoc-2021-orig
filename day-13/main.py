import numpy as np


def fold_sheet_up(sheet, fold_y) -> np.ndarray:
    shape = max(fold_y, sheet.shape[0] - fold_y - 1), sheet.shape[1]
    upper_portion = np.zeros(shape, dtype=bool)
    lower_portion = np.zeros(shape, dtype=bool)
    if fold_y >= sheet.shape[0] - fold_y - 1:
        upper_portion[0:fold_y - 1, 0:shape[1]] = sheet[0:fold_y - 1, 0:shape[1]]
        lower_portion[fold_y - (sheet.shape[0] - fold_y - 1):shape[0], 0:shape[1]] = sheet[-1:fold_y:-1, 0:shape[1]]
    else:
        upper_portion[shape[0] - fold_y:shape[0], 0:shape[1]] = sheet[0:fold_y, 0:shape[1]]
        lower_portion[0:shape[0] - fold_y - 1, 0:shape[1]] = sheet[-1:fold_y:-1, 0:shape[1]]
    return np.bitwise_or(upper_portion, lower_portion)


def fold_sheet_left(sheet, fold_x) -> np.ndarray:
    shape = sheet.shape[0], max(fold_x, sheet.shape[0] - fold_x - 1)
    left_portion = np.zeros(shape, dtype=bool)
    right_portion = np.zeros(shape, dtype=bool)
    if fold_x >= sheet.shape[1] - fold_x - 1:
        left_portion[0:shape[0], 0:fold_x] = sheet[0:shape[0], 0:fold_x]
        right_portion[0:shape[0], fold_x - (sheet.shape[1] - fold_x - 1):shape[1]] = sheet[0:shape[0], -1:fold_x:-1]
    else:
        left_portion[0:shape[0], shape[1] - fold_x:shape[1]] = sheet[0:shape[0], 0:fold_x]
        right_portion[0:shape[0], 0:shape[1] - fold_x - 1] = sheet[0:shape[0], -1:fold_x:-1]
    return np.bitwise_or(left_portion, right_portion)


def fold_sheet(sheet, axis, value) -> np.ndarray:
    if axis == 'x':
        return fold_sheet_left(sheet, value)
    else:
        return fold_sheet_up(sheet, value)


def read_input() -> (list, list, int, int):
    points = []
    folds = []
    max_x = 0
    max_y = 0
    with open('data.txt', 'r') as data_file:
        lines = data_file.read().splitlines()
        for line in lines:
            if ',' in line:
                x_str, y_str = line.strip().split(',')
                x = int(x_str)
                if x > max_x:
                    max_x = x
                y = int(y_str)
                if y > max_y:
                    max_y = y
                points.append((x, y))
            elif 'fold' in line:
                fields = line.strip().split(' ')
                axis, value = fields[-1].split('=')
                folds.append((axis, int(value)))
    return points, folds, max_x + 1, max_y + 1


def print_sheet(sheet) -> None:
    for y in range(sheet.shape[0]):
        for x in range(sheet.shape[1]):
            if sheet[y][x]:
                print('#', end='')
            else:
                print(' ', end='')
        print('')


def main() -> None:
    points, folds, width, height = read_input()
    sheet = np.zeros((height, width), dtype=bool)
    for x, y in points:
        sheet[y][x] = 1
    for i in range(len(folds)):
        sheet = fold_sheet(sheet, folds[i][0], folds[i][1])
        if i == 0:
            print('Part 1, total dots after 1 fold = {}'.format(np.count_nonzero(sheet)))

    print('Part 2, 8-letter code:')
    print_sheet(sheet)


main()
