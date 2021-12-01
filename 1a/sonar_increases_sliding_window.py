file = open('sonar_increases.data', 'r')
increase_count = 0

prev_value = None

while True:
    line = file.readline()
    if not line:
        break
    value = int(line)
    if prev_value is not None:
        if prev_value < value:
            increase_count += 1
    prev_value = value
file.close()
print("increase_count: {}".format(increase_count))
