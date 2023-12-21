import tkinter as tk
from tkinter import ttk
import math


class CommandFinder:
    def __init__(self, k1, k2, areas, m, num_segments, num_commands):
        self.k1 = k1
        self.k2 = k2
        self.areas = areas
        self.m = m
        self.num_segments = num_segments
        self.num_commands = num_commands

    def find_commands(self, current_segment=0, num_commands=-99):
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


class CommandFinderUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Command Finder")

        self.k1_var = tk.DoubleVar(value=0.2)
        self.k2_var = tk.DoubleVar(value=0.3)
        self.areas_var = tk.StringVar(
            value="0.1, 0.2, 0.15, 0.3, 0.5, 0.6, 0.22, 0.17, 0.29, 0.21, 0.24, 0.19")
        self.m_var = tk.DoubleVar(value=0.3)
        self.num_segments_var = tk.IntVar(
            value=len(self.areas_var.get().split(", ")))
        self.num_commands_var = tk.IntVar(value=10)

        self.create_widgets()

    def create_widgets(self):
        ttk.Label(self.master, text="k1:").grid(row=0, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.k1_var).grid(row=0, column=1)

        ttk.Label(self.master, text="k2:").grid(row=1, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.k2_var).grid(row=1, column=1)

        ttk.Label(
            self.master, text="Areas (comma-separated):").grid(row=2, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.areas_var).grid(
            row=2, column=1)

        ttk.Label(self.master, text="m:").grid(row=3, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.m_var).grid(row=3, column=1)

        ttk.Label(self.master, text="Number of Segments:").grid(
            row=4, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.num_segments_var).grid(
            row=4, column=1)

        ttk.Label(self.master, text="Number of Commands:").grid(
            row=5, column=0, sticky=tk.E)
        ttk.Entry(self.master, textvariable=self.num_commands_var).grid(
            row=5, column=1)

        ttk.Button(self.master, text="Find Commands", command=self.find_commands).grid(
            row=6, column=0, columnspan=2)

        self.result_label = ttk.Label(self.master, text="")
        self.result_label.grid(row=7, column=0, columnspan=2)

    def find_commands(self):
        k1_value = self.k1_var.get()
        k2_value = self.k2_var.get()
        areas_values = list(map(float, self.areas_var.get().split(", ")))
        m_value = self.m_var.get()
        num_segments_value = self.num_segments_var.get()
        num_commands_value = self.num_commands_var.get()

        command_finder = CommandFinder(
            k1_value, k2_value, areas_values, m_value, num_segments_value, num_commands_value)

        commands_per_segment = command_finder.find_commands()

        self.result_label.config(
            text=f"Кількість команд для кожного сегмента: {commands_per_segment}")


if __name__ == "__main__":
    root = tk.Tk()
    app = CommandFinderUI(root)
    root.mainloop()
