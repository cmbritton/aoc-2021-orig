import numpy
from scipy.ndimage.interpolation import shift


class Simulator(object):
    MAX_DAYS = 256
    SPAWN_CYCLE_DAYS = 7
    NEWBORN_SPAWN_DELAY_DAYS = 2
    AGE_BUCKET_SIZE = SPAWN_CYCLE_DAYS + NEWBORN_SPAWN_DELAY_DAYS + 1
    NEWBORN_CYCLE_DAYS = SPAWN_CYCLE_DAYS + NEWBORN_SPAWN_DELAY_DAYS

    def __init__(self, input_line):
        self.total_lantern_fish = 0
        init_ages_days = input_line.strip().split(',')
        self.generations = numpy.full(Simulator.AGE_BUCKET_SIZE, 0, dtype=numpy.uint)
        for i in range(len(init_ages_days)):
            self.generations[int(init_ages_days[i])] += 1
        self.day = 0

    def run(self):
        for day in range(Simulator.MAX_DAYS):
            self.tick()
            print('Total after {} days: {}'.format(self.day, numpy.sum(self.generations)))

    def tick(self):
        self.day += 1

        self.add_adolescents_to_adults()
        self.shift_young_generations()
        self.spawn()

    def spawn(self):
        spawn_index = (self.day - 1) % Simulator.SPAWN_CYCLE_DAYS
        print('spawning {} from generations {}'.format(self.generations[spawn_index], spawn_index))
        self.generations[Simulator.NEWBORN_CYCLE_DAYS] = self.generations[spawn_index]

    def add_adolescents_to_adults(self):
        # new_adult_index = (self.day - Simulator.NEWBORN_SPAWN_DELAY_DAYS - 1) % Simulator.SPAWN_CYCLE_DAYS
        new_adult_index = (self.day - 2) % Simulator.SPAWN_CYCLE_DAYS
        print('=============')
        print('day: {}, new_adult_index: {}, generations: {}'.format(self.day, new_adult_index, self.generations))
        print('adding {} spawned on day {} to {}'.format(self.generations[Simulator.NEWBORN_CYCLE_DAYS - 2],
                                                         self.day - Simulator.NEWBORN_SPAWN_DELAY_DAYS, new_adult_index))
        self.generations[new_adult_index] += self.generations[Simulator.NEWBORN_CYCLE_DAYS - 2]

    def shift_young_generations(self):
        print('before shift: {}'.format(self.generations))
        for i in range(Simulator.SPAWN_CYCLE_DAYS, Simulator.AGE_BUCKET_SIZE - 1):
            self.generations[i] = self.generations[i + 1]
        self.generations[Simulator.AGE_BUCKET_SIZE - 1] = 0
        # shift(self.generations[Simulator.SPAWN_CYCLE_DAYS:], -1, cval=0)
        print('after shift:  {}'.format(self.generations))


def run():
    numpy.set_printoptions(linewidth=1000)
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        simulator = Simulator(input_line)
        simulator.run()


def main():
    run()


main()
