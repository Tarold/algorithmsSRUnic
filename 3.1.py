import tkinter as tk

class Greedy:
    def __init__(self, products=None):
        if products == None:
            self.products = []
        else:
            self.products = products


    def add_product(self, name, price, expiry_date):
        self.products.append((name, price, expiry_date))


    def del_product(self, index):
        try:
            del self.products[index]
            self.print_to_ui("Product successful deleted!")
        except IndexError:
            self.print_to_ui('Invalid index')


    def edit_product(self, index, name, price, expiry_date):
        try:
            self.products[index] = (name, price, expiry_date)
            self.print_to_ui("Product successfully edited!")
        except IndexError:
            self.print_to_ui("Invalid index")


    def display_products(self):
        if len(self.products) > 0:
            self.print_to_ui()
            for index, product in enumerate(self.products):
                name, price, expiry_date = product
                self.print_to_ui(
                    f'{index}) Name: {name}, Price: {price}, Expiry date: {expiry_date}', True)
        else:
            self.print_to_ui("List of products is empty")


    def solve_task(self):
        if len(self.products) > 0:
            total_profit = 0
            total_loss = 0
            days_gone = 0


            self.products.sort(key=lambda x: x[1]/x[2], reverse=True)

            self.print_to_ui('List:')
            for product in self.products:
                name, price, expiry_date = product
                
                self.print_to_ui(
                    f'Name: {name}, Price: {price}, Expiry date: {expiry_date}', True)
                

                if expiry_date - days_gone > 0:
                    total_profit += price
                else:
                    total_profit += price / 2
                    total_loss += price / 2


                days_gone += 1


            self.print_to_ui(f'Total profit:{total_profit}, Total loss:{total_loss}', True)
        else:
            self.print_to_ui("List of products is empty")

    def set_output_widget(self, output_widget):
        self.output_widget = output_widget

    def print_to_ui(self, message='', isNotDel=False):
        if hasattr(self, 'output_widget'):
            if (isNotDel==False): self.output_widget.delete(1.0, tk.END)
            self.output_widget.insert(tk.END, message + "\n")
        else:
            print(message)

class GreedyUI(tk.Tk):
    def __init__(self, products=None):
        super().__init__()

        if products is None:
            products = []

        self.greedy = Greedy(products)

        self.title("Greedy UI")
        self.geometry("400x400")

        self.create_widgets()

    def create_widgets(self):
        self.label = tk.Label(self, text="Greedy UI")
        self.label.pack(pady=10)

        self.output_text = tk.Text(self, height=10, width=40)
        self.output_text.pack(pady=10, expand=1, fill="both")

        self.display_button = tk.Button(self, text="Display Products", command=self.display_products)
        self.display_button.pack()

        self.solve_button = tk.Button(self, text="Solve Task", command=self.solve_task)
        self.solve_button.pack()

        self.add_button = tk.Button(self, text="Add Product", command=self.add_product_window)
        self.add_button.pack()

        self.edit_button = tk.Button(self, text="Edit Product", command=self.edit_product_window)
        self.edit_button.pack()

        self.del_button = tk.Button(self, text="Delete Product", command=self.del_product_window)
        self.del_button.pack()

        self.greedy.set_output_widget(self.output_text)

    def display_products(self):
        self.greedy.display_products()

    def solve_task(self):
        self.greedy.solve_task()

    def add_product_window(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Product")

        name_label = tk.Label(add_window, text="Name:")
        name_label.grid(row=0, column=0)
        name_entry = tk.Entry(add_window)
        name_entry.grid(row=0, column=1)

        price_label = tk.Label(add_window, text="Price:")
        price_label.grid(row=1, column=0)
        price_entry = tk.Entry(add_window)
        price_entry.grid(row=1, column=1)

        expiry_label = tk.Label(add_window, text="Expiry Date:")
        expiry_label.grid(row=2, column=0)
        expiry_entry = tk.Entry(add_window)
        expiry_entry.grid(row=2, column=1)

        add_button = tk.Button(add_window, text="Add", command=lambda: self.add_product(
            name_entry.get(), float(price_entry.get()), int(expiry_entry.get()), add_window))
        add_button.grid(row=3, column=0, columnspan=2, pady=10)

    def add_product(self, name, price, expiry_date, window):
        self.greedy.add_product(name, price, expiry_date)
        self.display_products()
        window.destroy()

    def edit_product_window(self):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Product")

        index_label = tk.Label(edit_window, text="Index:")
        index_label.grid(row=0, column=0)
        index_entry = tk.Entry(edit_window)
        index_entry.grid(row=0, column=1)

        name_label = tk.Label(edit_window, text="Name:")
        name_label.grid(row=1, column=0)
        name_entry = tk.Entry(edit_window)
        name_entry.grid(row=1, column=1)

        price_label = tk.Label(edit_window, text="Price:")
        price_label.grid(row=2, column=0)
        price_entry = tk.Entry(edit_window)
        price_entry.grid(row=2, column=1)

        expiry_label = tk.Label(edit_window, text="Expiry Date:")
        expiry_label.grid(row=3, column=0)
        expiry_entry = tk.Entry(edit_window)
        expiry_entry.grid(row=3, column=1)

        edit_button = tk.Button(edit_window, text="Edit", command=lambda: self.edit_product(
            int(index_entry.get()), name_entry.get(), float(price_entry.get()), int(expiry_entry.get()), edit_window))
        edit_button.grid(row=4, column=0, columnspan=2, pady=10)

    def edit_product(self, index, name, price, expiry_date, window):
        self.greedy.edit_product(index, name, price, expiry_date)
        self.display_products()
        window.destroy()

    def del_product_window(self):
        del_window = tk.Toplevel(self)
        del_window.title("Delete Product")

        index_label = tk.Label(del_window, text="Index:")
        index_label.grid(row=0, column=0)
        index_entry = tk.Entry(del_window)
        index_entry.grid(row=0, column=1)

        del_button = tk.Button(del_window, text="Delete", command=lambda: self.del_product(
            int(index_entry.get()), del_window))
        del_button.grid(row=1, column=0, columnspan=2, pady=10)

    def del_product(self, index, window):
        self.greedy.del_product(index)
        self.display_products()
        window.destroy()

if __name__ == "__main__":
    products = [("Product-1", 14, 3), ("Product-2", 11, 2),
                ("Product-3", 9, 2), ("Product-4", 13, 3), ("Product-5", 10, 2)]
    app = GreedyUI(products)
    app.mainloop()
