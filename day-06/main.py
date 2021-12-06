
class LanternFish(object):
    SPAWN_CYCLE_DAYS = 7
    NEWBORN_SPAWN_DELAY_DAYS = 2

    def __init__(self, age_days):
        self.age_days = age_days

    def add_data(self, input_line):
        pass

    def to_string(self):
        return '{}'.format(self.age_days)


class Simulator(object):
    MAX_DAYS = 256
    PART_1_DAYS = 80
    PART_2_DAYS = 256

    def __init__(self):
        self.all_lantern_fish = []
        self.newborn_lantern_fish = []
        self.day = 0

    def create_lantern_fish(self, age_days):
        self.all_lantern_fish.append(LanternFish(age_days))

    def create_newborn_lantern_fish(self):
        self.newborn_lantern_fish.append(
            LanternFish(LanternFish.SPAWN_CYCLE_DAYS + LanternFish.NEWBORN_SPAWN_DELAY_DAYS - 1))

    def run(self):
        for day in range(Simulator.MAX_DAYS):
            self.tick()
            if day == Simulator.PART_1_DAYS - 1:
                self.print_result()
            if day == Simulator.PART_2_DAYS - 1:
                self.print_result()

    def tick(self):
        self.day += 1
        for lantern_fish in self.all_lantern_fish:
            lantern_fish.age_days -= 1
            if lantern_fish.age_days < 0:
                lantern_fish.age_days = LanternFish.SPAWN_CYCLE_DAYS - 1
                self.create_newborn_lantern_fish()
        self.all_lantern_fish.extend(self.newborn_lantern_fish)
        self.newborn_lantern_fish.clear()

    def print_result(self):
        print('Total after {} days: {}'.format(self.day, len(self.all_lantern_fish)))

    def to_string(self):
        result = ''
        for lantern_fish in self.all_lantern_fish:
            result += lantern_fish.to_string()
            result += '\n'
        return result


def run():
    simulator = Simulator()
    with open('data.txt', 'r') as data_file:
        input_line = data_file.readline()
        init_ages_days = input_line.strip().split(',')
        for age in init_ages_days:
            simulator.create_lantern_fish(int(age))
        simulator.run()


def main():
    run()


main()
