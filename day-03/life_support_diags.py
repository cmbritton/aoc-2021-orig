class LifeSupportDiagnostics(object):
    LENGTH = 12

    def __init__(self):
        self.values = []
        self.zeroCount = [0] * LifeSupportDiagnostics.LENGTH
        self.oneCount = [0] * LifeSupportDiagnostics.LENGTH

    def oxygen_rating(self):
        oxygen_values = self.values.copy()
        return self.reduce_values(oxygen_values, self.most_common_value)

    def co2_rating(self):
        co2_values = self.values.copy()
        return self.reduce_values(co2_values, self.least_common_value)

    def reduce_values(self, values, bit_criteria_function):
        for position in range(LifeSupportDiagnostics.LENGTH):
            self.discard_values(values, position, bit_criteria_function)
            if len(values) == 1:
                return values[0]

    def discard_values(self, values, position, bit_criteria_function):
        index = 0
        bit_value = bit_criteria_function(values, position)
        while index < len(values):
            if len(values) == 1:
                return
            if self.get_bit(values[index], position) != bit_value:
                del values[index]
                continue
            index += 1

    def get_bit(self, value, position):
        return (value >> LifeSupportDiagnostics.LENGTH - position - 1) & 1

    def position_counts(self, values, position):
        zero_count = 0
        one_count = 0
        for value in values:
            if self.get_bit(value, position):
                one_count += 1
            else:
                zero_count += 1
        return [zero_count, one_count]

    def most_common_value(self, values, position):
        [zero_count, one_count] = self.position_counts(values, position)
        return 1 if one_count >= zero_count else 0

    def least_common_value(self, values, position):
        [zero_count, one_count] = self.position_counts(values, position)
        return 0 if zero_count <= one_count else 1

    def rating(self):
        return self.oxygen_rating() * self.co2_rating()


def main():
    life_support_diagnostics = LifeSupportDiagnostics()
    with open('diagnostics.data', 'r') as data_file:
        line = data_file.readline()
        while line:
            value = line.strip()
            life_support_diagnostics.values.append(int(value, 2))
            line = data_file.readline()
    print("value: {}".format(life_support_diagnostics.rating()))


main()
