import tkinter as tk
from tkinter import ttk

class Game:
    def __init__(self, x, y, values):
        self.n1 = len(values)
        self.n2 = len(values[0]) if len(values) > 0 else 0
        self.xf = x
        self.yf = y
        self.values = values

    def findCost(self, path):
        cost = 0
        for i in range(0, len(path)):
            cost += path[i][2]
        return cost if cost != 0 else float('inf')

    def pathFinder(self, x, y, pathList):
        pathsList = [[], [], []]
        if x < 0 or y < 0 or x >= self.n2 or y >= self.n1:
            return []

        if (x == self.xf and y == self.yf):
            return pathList + [[x, y, 0, 'final']]
        
        if y + 1 < self.n1:
            pathsList[0] = self.pathFinder(
                x, y + 1, pathList + [[x, y, self.values[y + 1][x], 'Down']])
        if x + 1 < self.n2:
            pathsList[1] = self.pathFinder(
                x + 1, y, pathList + [[x, y, self.values[y][x + 1], 'Right']])
        if y + 1 < self.n1 and x + 1 < self.n2:
            pathsList[2] = self.pathFinder(
                x + 1, y + 1, pathList + [[x, y, self.values[y + 1][x + 1], 'Right/Down']])

        path = pathsList[0]
        for i in range(1, len(pathsList)):
            if self.findCost(pathsList[i]) < self.findCost(path):
                path = pathsList[i]

        return path

    def solve(self, x1, y1):
        if (x1 > self.xf) or (y1 > self.yf):
            print("Path is none")
            return
        path = self.pathFinder(x1, y1, [[x1, y1, 0, 'start']])
        return path

    def set_parameters(self, x, y, values):
        self.n1 = len(values)
        self.n2 = len(values[0]) if len(values) > 0 else 0
        self.xf = x
        self.yf = y
        self.values = values

    def update_value(self, x, y, new_value):
        if 0 <= x < self.n1 and 0 <= y < self.n2:
            self.values[y][x] = new_value
        else:
            print("Invalid coordinates")


class GameGUI:
    def __init__(self, master, game):
        self.master = master
        self.master.title("Game Visualization")
        self.start = [1, 0]
        self.game = game
        self.path_string_var = tk.StringVar()

        # Создаем вкладки
        self.tabControl = ttk.Notebook(self.master)

        # Вкладка 1: Ввод инициальных значений
        self.tab1 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='Initial Values')

        # Создаем виджеты для ввода строки с массивами
        self.values_entry = tk.Entry(self.tab1, width=20)
        self.values_entry.insert(0, "[[1, 1, 1], [2, 9, 2], [3, 3, 3]]")

        self.values_entry.grid(row=0, column=1, padx=5, pady=5)

        self.label_values = tk.Label(self.tab1, text='Values:')
        self.label_values.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)

        self.start_entry = tk.Entry(self.tab1, width=5)
        self.start_entry.insert(0, "1, 0")  # Дефолтные значения старта
        self.start_entry.grid(row=1, column=1, padx=5, pady=5)
        self.label_start = tk.Label(self.tab1, text='Start:')
        self.label_start.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)

        self.finish_entry = tk.Entry(self.tab1, width=5)
        self.finish_entry.insert(0, "2, 2")  # Дефолтные значения финиша
        self.finish_entry.grid(row=2, column=1, padx=5, pady=5)
        self.label_finish = tk.Label(self.tab1, text='Finish:')
        self.label_finish.grid(row=2, column=0, padx=5, pady=5, sticky=tk.E)

        self.submit_button = tk.Button(self.tab1, text="Submit", command=self.submit_values)
        self.submit_button.grid(row=3, column=1, pady=10)

        # Вкладка 2: Визуализация игры
        self.tab2 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab2, text='Game Visualization')

        self.canvas = tk.Canvas(self.tab2, width=300, height=200)
        self.canvas.grid(row=0, column=0, pady=10)

        self.find_path_button = tk.Button(self.tab2, text="Find Path", command=self.find_path)
        self.find_path_button.grid(row=1, column=0, pady=10)

        # Виджет для отображения значения клетки
        self.cell_value_label = tk.Label(self.tab2, text="")
        self.cell_value_label.grid(row=2, column=0, pady=5)

        # Вывод пути буквами
        self.path_label = tk.Label(self.tab2, textvariable=self.path_string_var)
        self.path_label.grid(row=3, column=0, pady=10)

        self.tabControl.pack(expand=1, fill="both")

    def submit_values(self):
        values_str = self.values_entry.get()
        values = eval(values_str)

        start_str = self.start_entry.get()

        finish_str = self.finish_entry.get()
        finish = tuple(map(int, finish_str.split(',')))

        self.game.set_parameters(finish[0], finish[1], values)
        self.start = tuple(map(int, start_str.split(',')))
        
    def find_path(self):
        path = self.game.solve(self.start[0], self.start[1])
        print("Path:", path)
        self.draw_path_on_canvas(path)
        self.display_path_string(path)

    def draw_path_on_canvas(self, path):
        self.canvas.delete("all")
        for i in range(len(self.game.values)):
            for j in range(len(self.game.values[0])):
                x, y = j * 30, i * 30
                self.canvas.create_rectangle(x, y, x + 30, y + 30, outline="black", fill="white")
                self.canvas.create_text(x + 15, y + 15, text=str(self.game.values[i][j]))

        for step in path:
            x, y = step[0] * 30, step[1] * 30
            self.canvas.create_rectangle(x, y, x + 30, y + 30, outline="black", fill="yellow")
            self.canvas.create_text(x + 15, y + 15, text=str(self.game.values[step[1]][step[0]]))

        start_x, start_y = path[0][0] * 30, path[0][1] * 30
        self.canvas.create_rectangle(start_x, start_y, start_x + 30, start_y + 30, outline="black", fill="green")
        self.canvas.create_text(x + 15, y + 15, text=str(self.game.values[i][j]))

        end_x, end_y = path[-1][0] * 30, path[-1][1] * 30
        self.canvas.create_rectangle(end_x, end_y, end_x + 30, end_y + 30, outline="black", fill="red")
        self.canvas.create_text(x + 15, y + 15, text=str(self.game.values[i][j]))

        # Отображение значения выбранной ячейки
        self.cell_value_label.config(text=f"Path Value: {self.game.findCost(path)}")

    def display_path_string(self, path):
        path_str = ""
        for step in path:
            path_str += step[3] + ', '  # Используем направление (Down, Right, Right/Down)
        self.path_string_var.set(f"Path: {path_str}")

if __name__ == "__main__":
    values = [[1, 1, 1], [2, 9, 2], [3, 3, 3]]
    game = Game(2, 2, values)
    root = tk.Tk()
    app = GameGUI(root, game)
    root.mainloop()
