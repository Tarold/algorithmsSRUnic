import tkinter as tk
from tkinter import ttk

class HashTable:
    def __init__(self, size=10):
        self.size = size
        self.table = [None] * size

    def hash_function(self, key):
        return hash(key) % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        while self.table[index] is not None:
            if self.table[index][0] == key:
                self.table[index][1] = value
                break
            index = (index + 1) % self.size
        else:
            self.table[index] = [key, value]

    def delete(self, key):
        index = self.hash_function(key) % len(self.table)
        if self.table[index] is not None and self.table[index][0] == key:
            self.table[index] = None
        else:
            del_index = self.search_index(key)
            self.table[del_index] = None

    def search_index(self, key):
        initial_index = self.hash_function(key) % len(self.table)
        for i in range(len(self.table)):
            index = (initial_index + i) % len(self.table)
            if self.table[index][0] == key:
                return index

    def search(self, key):
        return self.table[self.search_index(key)][1]

    def display(self):
        for i, bucket in enumerate(self.table):
            if bucket is not None:
                print(f"Index: {i}, Bucket: {bucket[0]} = {bucket[1]}")
            else:
                print(f"Index {i}:")

class HashTableUI:
    def __init__(self, master, hash_table):
        self.master = master
        self.master.title("HashTable UI")
        self.hash_table = hash_table

        self.tabControl = ttk.Notebook(self.master)

        # Insert Tab
        self.insertTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.insertTab, text='Insert')
        self.insert_label = tk.Label(self.insertTab, text="Key:")
        self.insert_label.pack()
        self.insert_key_entry = tk.Entry(self.insertTab)
        self.insert_key_entry.pack()
        self.insert_value_label = tk.Label(self.insertTab, text="Value:")
        self.insert_value_label.pack()
        self.insert_value_entry = tk.Entry(self.insertTab)
        self.insert_value_entry.pack()
        self.insert_button = tk.Button(self.insertTab, text="Insert", command=self.insert)
        self.insert_button.pack()
        self.insert_status_label = tk.Label(self.insertTab, text="")
        self.insert_status_label.pack()

        # Delete Tab
        self.deleteTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.deleteTab, text='Delete')
        self.delete_label = tk.Label(self.deleteTab, text="Key:")
        self.delete_label.pack()
        self.delete_key_entry = tk.Entry(self.deleteTab)
        self.delete_key_entry.pack()
        self.delete_button = tk.Button(self.deleteTab, text="Delete", command=self.delete)
        self.delete_button.pack()
        self.delete_status_label = tk.Label(self.deleteTab, text="")
        self.delete_status_label.pack()

        # Search Tab
        self.searchTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.searchTab, text='Search')
        self.search_label = tk.Label(self.searchTab, text="Key:")
        self.search_label.pack()
        self.search_key_entry = tk.Entry(self.searchTab)
        self.search_key_entry.pack()
        self.search_button = tk.Button(self.searchTab, text="Search", command=self.search)
        self.search_button.pack()
        self.search_result_label = tk.Label(self.searchTab, text="")
        self.search_result_label.pack()

        # Display Tab
        self.displayTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.displayTab, text='Display')
        self.display_text = tk.Text(self.displayTab, wrap=tk.WORD)
        self.display_text.pack()
        self.display_button = tk.Button(self.displayTab, text="Display", command=self.display)
        self.display_button.pack()

        self.tabControl.pack(expand=1, fill="both")
        self.tabControl.bind("<<NotebookTabChanged>>", self.tab_changed)

    def tab_changed(self, event):
        selected_tab_index = self.tabControl.index(self.tabControl.select())
        if selected_tab_index == 3:
            self.display()

    def insert(self):
        key = self.insert_key_entry.get()
        value = self.insert_value_entry.get()
        self.hash_table.insert(key, value)
        self.insert_status_label.config(text="Insertion successful")
        self.display()

    def delete(self):
        key = self.delete_key_entry.get()
        try:
            self.hash_table.delete(key)
            self.delete_status_label.config(text="Deletion successful")
        except:
            self.delete_status_label.config(text="Key not found")
        self.display()

    def search(self):
        key = self.search_key_entry.get()
        try:
            result = self.hash_table.search(key)
            self.search_result_label.config(text=f"Result: {result}")
        except:
            self.search_result_label.config(text="Key not found")

    def display(self):
        self.display_text.delete(1.0, tk.END)
        output = ""
        for i, bucket in enumerate(self.hash_table.table):
            if bucket is not None:
                output += f"Index: {i}, Bucket: {bucket[0]} = {bucket[1]}\n"
            else:
                output += f"Index: {i}, None\n"
        self.display_text.insert(tk.END, output)

def build_hash_table(file_path):
    hash_table = HashTable()
    with open(file_path, 'r', encoding="utf-8") as file:
        for line in file:
            key, value = line.strip().split(', ')
            hash_table.insert(key, value)
    return hash_table

def main():
    hash_table = build_hash_table('2.1.txt')

    root = tk.Tk()
    app = HashTableUI(root, hash_table)
    root.mainloop()

if __name__ == "__main__":
    main()
