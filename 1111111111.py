import math

class CommandFinder:
    def __init__(self, k1, k2, areas, m, num_segments, num_commands):
        self.k1 = k1
        self.k2 = k2
        self.areas = areas
        self.m = m
        self.num_segments = num_segments
        self.num_commands = num_commands

    def find_commands(self,  current_segment=0, num_commands=-99):
        if (num_commands < 0):
            num_commands = self.num_commands
        if current_segment == self.num_segments:
            return [0] * (self.num_segments - current_segment)

        probability = self.probability_function(
            self.k1, self.k2, self.areas[current_segment], self.m)

        commands_for_segment = math.ceil(probability * num_commands)

        list_of_commands = []
        for else_commands_variants in range(commands_for_segment, -1, -1):
            remaining_commands = num_commands - else_commands_variants

            list_of_commands.append([else_commands_variants] + self.find_commands(
                current_segment + 1, remaining_commands))

        return self.give_most_probability(list_of_commands)

    def give_most_probability(self, commands_list):
        list_probability = []

        for commands in commands_list:
            a = 0
            for command in commands:
                if a == 0:
                    a = self.probability_function(
                        self.k1, self.k2, self.areas[len(list_probability)], command)
                else:
                    a = (a + self.probability_function(self.k1, self.k2,
                         self.areas[len(list_probability)], command)) / 2
            list_probability.append(a)

        return commands_list[list_probability.index(max(list_probability))]

    def probability_function(self, k1, k2, s, m):
        return math.exp(-k1 * s) * (1 - math.exp(-k2 * m))

    def update_values(self, k1=None, k2=None, areas=None, m=None, num_segments=None, num_commands=None):
        if k1 is not None:
            self.k1 = k1
        if k2 is not None:
            self.k2 = k2
        if areas is not None:
            self.areas = areas
        if m is not None:
            self.m = m
        if num_segments is not None:
            self.num_segments = num_segments
        if num_commands is not None:
            self.num_commands = num_commands

k1_value = 0.2
k2_value = 0.3
areas_values = [0.1, 0.2, 0.15, 0.3, 0.5,
                0.6, 0.22, 0.17, 0.29, 0.21, 0.24, 0.19]
m_value = 0.3
num_segments_value = len(areas_values)
num_commands_value = 10

command_finder = CommandFinder(
    k1_value, k2_value, areas_values, m_value, num_segments_value, num_commands_value)

commands_per_segment = command_finder.find_commands()

print("Кількість команд для кожного сегмента:", commands_per_segment)

# Приклад зміни значень
command_finder.update_values(k1=0.5, m=0.4)
updated_commands_per_segment = command_finder.find_commands()

print("Оновлені кількості команд для кожного сегмента:", updated_commands_per_segment)
