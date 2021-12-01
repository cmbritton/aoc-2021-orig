from collections import deque

WINDOW_SIZE = 3

sliding_window = deque()

prev_total = None

increase_count = 0

file = open('sonar_increases.data', 'r')
while True:
    line = file.readline()
    if not line:
        break
    input_value = int(line)
    sliding_window.append(input_value)
    if len(sliding_window) > WINDOW_SIZE:
        sliding_window.popleft()
    if len(sliding_window) == WINDOW_SIZE:
        total = 0
        if prev_total is not None:
            for value in sliding_window:
                total += value
            if prev_total < total:
                increase_count += 1
        prev_total = total
file.close()
print("increase_count: {}".format(increase_count))


class SlidingWindow:
    WINDOW_SIZE = 3
    window = deque()
