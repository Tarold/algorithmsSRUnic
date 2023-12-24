import os
import tkinter as tk
from tkinter import ttk, messagebox
import subprocess
from PIL import Image, ImageTk
from threading import Thread


class MainApplication(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Самостоятельная работа КНТ113СП")
        self.geometry("800x600")

        self.create_menu()

        self.tabControl = ttk.Notebook(self)

        self.show_main_content(
            "Самостоятельная работа №1\nСтудент: КНТ113СП Олексій Сімічов")

    def create_menu(self):
        menu_bar = tk.Menu(self)

        for i in range(1, 7):
            sub_menu = tk.Menu(menu_bar, tearoff=0)
            menu_bar.add_cascade(label=f"{i} ЛР", menu=sub_menu)
            for t in [1, 2] if (i != 5) else [1, 2, 3]:
                img = f"{i}.{t}.png"
                sub_menu.add_command(
                    label=f"Задание {t}", command=lambda i=i, t=t: self.run_task(i, t))
                sub_menu.add_command(
                    label=f"Показать фото {t}", command=lambda img=img: self.show_image(img))

        self.config(menu=menu_bar)

    def run_task(self, lab_number, task_number):
        thread = Thread(target=self._run_task, args=(lab_number, task_number))
        thread.start()

    def _run_task(self, lab_number, task_number):
        script_path = f"{lab_number}.{task_number}.py"

        if not os.path.exists(script_path):
            messagebox.showerror("Ошибка", "Файл с заданием не найден.")
            return

        subprocess.run(["python3", script_path])

    def show_image(self, image_path):
        thread = Thread(target=self._show_image, args=(image_path,))
        thread.start()

    def _show_image(self, image_path):
        image = Image.open(image_path)

        image_window = tk.Toplevel(self)
        image_window.title("Фото с заданием")

        tk_image = ImageTk.PhotoImage(image)
        label = tk.Label(image_window, image=tk_image)
        label.image = tk_image
        label.pack()

    def show_main_content(self, content):
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True)

        label = tk.Label(main_frame, text=content, padx=10, pady=10)
        label.pack()

        self.tabControl.pack(in_=main_frame, side="top",
                             fill="both", expand=True)

    def run(self):
        self.mainloop()


if __name__ == "__main__":
    app = MainApplication()
    app.run()
