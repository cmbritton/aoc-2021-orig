import numpy
from time import process_time


class Simulator(object):
    MAX_SIZE = 300000
    MAX_DAYS = 256
    SPAWN_CYCLE_DAYS = 7
    NEWBORN_SPAWN_DELAY_DAYS = 2
    NEWBORN_CYCLE_DAYS = SPAWN_CYCLE_DAYS + NEWBORN_SPAWN_DELAY_DAYS

    def __init__(self, input_line):
        self.total_lantern_fish = 0
        init_ages_days = input_line.strip().split(',')
        self.all_lantern_fish = numpy.full(Simulator.MAX_SIZE, -2, dtype=numpy.int8)
        for i in range(len(init_ages_days)):
            self.all_lantern_fish[i] = int(init_ages_days[i])
            self.total_lantern_fish += 1
        self.day = 0

    def run(self):
        for day in range(Simulator.MAX_DAYS):
            start_time = process_time()
            self.tick()
            end_time = process_time()
            print('Total after {} days: {}'.format(self.day, self.total_lantern_fish))
            print('    elapsed time: {} seconds'.format(end_time - start_time))

    def tick(self):
        self.day += 1
        self.all_lantern_fish[self.all_lantern_fish >= 0] -= 1
        newborn_count = (self.all_lantern_fish == -1).sum()
        self.all_lantern_fish[self.all_lantern_fish == -1] = Simulator.SPAWN_CYCLE_DAYS - 1
        if newborn_count:
            self.all_lantern_fish[self.total_lantern_fish:self.total_lantern_fish + newborn_count] = Simulator.NEWBORN_CYCLE_DAYS - 1
            self.total_lantern_fish += newborn_count

    def print_result(self):
        print('Total after {} days: {}'.format(self.day, len(self.all_lantern_fish)))


def run():
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        simulator = Simulator(input_line)
        simulator.run()


def main():
    run()


main()
