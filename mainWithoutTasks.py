import os
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import subprocess

class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Самостоятельная работа КНТ113СП")
        self.geometry("800x600")

        self.create_menu()

        self.tabControl = ttk.Notebook(self)

        self.create_tab("Главная", "Приветствие и объяснение задания")
        self.create_tab_with_tasks("1 ЛР", [1, 2])
        self.create_tab_with_tasks("2 ЛР", [1, 2])
        self.create_tab_with_tasks("3 ЛР", [1, 2])
        self.create_tab_with_tasks("4 ЛР", [1, 2])
        self.create_tab_with_tasks("5 ЛР", [1, 2])
        self.create_tab_with_tasks("6 ЛР", [1, 2])

    def create_menu(self):
        menu_bar = tk.Menu(self)

        for i in range(1, 7):
            sub_menu = tk.Menu(menu_bar, tearoff=0)
            menu_bar.add_cascade(label=f"{i} ЛР", menu=sub_menu)
            sub_menu.add_command(label="Задание 1", command=lambda i=i, t=1: self.run_task(i, t))
            sub_menu.add_command(label="Задание 2", command=lambda i=i, t=2: self.run_task(i, t))

        self.config(menu=menu_bar)

    def create_tab(self, title, content):
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text=title)

        label = tk.Label(tab, text=content, padx=10, pady=10)
        label.pack()

    def create_tab_with_tasks(self, title, tasks):
        tab = ttk.Frame(self.tabControl)
        self.tabControl.add(tab, text=title)

        task_listbox = tk.Listbox(tab)
        for task in tasks:
            task_listbox.insert(tk.END, f"Задание {task}")

        task_listbox.bind("<ButtonRelease-1>", self.on_task_click)
        task_listbox.pack(padx=10, pady=10)

    def run_task(self, lab_number, task_number):
        script_path = os.path.join(os.path.dirname(__file__), f"{lab_number}.{task_number}.py")

        if os.path.exists(script_path):
            subprocess.run(["python3", script_path])
        else:
            messagebox.showerror("Ошибка", "Файл с заданием не найден.")

    def on_task_click(self, event):
        selected_task = event.widget.get(event.widget.curselection())
        lab_number, task_number = selected_task.split()[1].split('.')
        self.run_task(int(lab_number), int(task_number))

    def run(self):
        self.mainloop()

if __name__ == "__main__":
    app = MainApplication()
    app.run()
