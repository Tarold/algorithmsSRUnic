import tkinter as tk
from tkinter import ttk

class Car:
    def __init__(self, vin, registration_date, owner):
        self.vin = vin
        self.registration_date = registration_date
        self.owner = owner

    def __repr__(self):
        return f"Car(vin={self.vin}, registration_date={self.registration_date}, owner={self.owner})"

class Node:
    def __init__(self, key=None):
        self.key = key
        self.leftChild = None
        self.rightChild = None
        self.parent = None

    def hasLeft(self):
        return self.leftChild is not None

    def hasRight(self):
        return self.rightChild is not None

    def hasNoChildren(self):
        return self.leftChild is None and self.rightChild is None

    def setNode(self, item):
        if isinstance(item, Node):
            self.key = item.key
            self.leftChild = item.leftChild
            self.rightChild = item.rightChild
        else:
            self.key = item

    def setLeft(self, item):
        if isinstance(item, Node):
            self.leftChild = item
        elif self.hasLeft():
            self.leftChild.setNode(item)
        else:
            self.leftChild = Node(item)
            self.leftChild.parent = self

    def setRight(self, item):
        if isinstance(item, Node):
            self.rightChild = item
        elif self.hasRight():
            self.rightChild.setNode(item)
        else:
            self.rightChild = Node(item)
            self.rightChild.parent = self

    def __repr__(self):
        if self.key is None:
            return "None"
        return f"Node(key={self.key})"

class BinaryTree(Node):
    def search(self, vin):
        if self.key is None:
            return None
        node = self
        while node is not None:
            if vin == node.key.vin:
                return node
            elif vin < node.key.vin:
                node = node.leftChild
            else:
                node = node.rightChild
        return None

    def insert(self, key):
        if self.key is None:
            self.key = key
        node = self
        while True:
            if node.key.vin == key.vin:
                break
            elif node.key.vin < key.vin:
                if node.hasRight():
                    node = node.rightChild
                else:
                    node.setRight(key)
                    break
            else:
                if node.hasLeft():
                    node = node.leftChild
                else:
                    node.setLeft(key)
                    break

    def delete(self, vin):
        node = self.search(vin)
        if node is None:
            return
        if node.hasNoChildren():
            if node.parent is None:
                node.key = None
            else:
                if node.parent.leftChild == node:
                    node.parent.leftChild = None
                else:
                    node.parent.rightChild = None
        elif node.hasRight() and not node.hasLeft():
            node.setNode(node.rightChild)
        elif node.hasLeft() and not node.hasRight():
            node.setNode(node.leftChild)
        else:
            if node.leftChild.hasRight():
                wNode = node.leftChild.rightChild
                while True:
                    if wNode.hasRight():
                        wNode = wNode.rightChild
                    else:
                        node.setNode(wNode)
                        wNode.parent.rightChild = None
                        return
            else:
                if node.leftChild.hasNoChildren():
                    node.setNode(node.leftChild)
                else:
                    resultNode = node.leftChild
                    self.delete(node.leftChild)
                    node.setNode(resultNode)

    def find_owners_with_multiple_cars(self):
        owners = []
        allOwners = []

        def _find_owners_with_multiple_cars(node):
            if node is None:
                return
            if node.key is not None:
                if (node.key.owner in allOwners) and (node.key.owner not in owners):
                    owners.append(node.key.owner)
                else:
                    allOwners.append(node.key.owner)
            _find_owners_with_multiple_cars(node.leftChild)
            _find_owners_with_multiple_cars(node.rightChild)

        _find_owners_with_multiple_cars(self)
        return owners

    def display(self, node=None, level=0, side=None):
        if node is None:
            node = self
        if self.key is not None:
            if level == 0:
                print(" " * level + repr(node.key))
            else:
                if side == "left":
                    postfix = "├── " + repr(node.key)
                elif side == "right":
                    postfix = "└── " + repr(node.key)
                print(" " * (level - 1) + postfix)
            if node.leftChild:
                self.display(node.leftChild, level + 1, side="left")
            if node.rightChild:
                self.display(node.rightChild, level + 1, side="right")

class BinaryTreeUI:
    def __init__(self, master, tree):
        self.master = master
        self.master.title("Binary Tree UI")
        self.tree = tree
        self.current_tab = None

        self.tabControl = ttk.Notebook(self.master)

        # Insert Tab
        self.insertTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.insertTab, text='Insert')
        self.insert_label = tk.Label(self.insertTab, text="VIN:")
        self.insert_label.pack()
        self.insert_vin_entry = tk.Entry(self.insertTab)
        self.insert_vin_entry.pack()
        self.insert_date_label = tk.Label(self.insertTab, text="Registration Date:")
        self.insert_date_label.pack()
        self.insert_date_entry = tk.Entry(self.insertTab)
        self.insert_date_entry.pack()
        self.insert_owner_label = tk.Label(self.insertTab, text="Owner:")
        self.insert_owner_label.pack()
        self.insert_owner_entry = tk.Entry(self.insertTab)
        self.insert_owner_entry.pack()
        self.insert_button = tk.Button(self.insertTab, text="Insert", command=self.insert)
        self.insert_button.pack()
        self.insert_status_label = tk.Label(self.insertTab, text="")
        self.insert_status_label.pack()

        # Delete Tab
        self.deleteTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.deleteTab, text='Delete')
        self.delete_label = tk.Label(self.deleteTab, text="VIN:")
        self.delete_label.pack()
        self.delete_vin_entry = tk.Entry(self.deleteTab)
        self.delete_vin_entry.pack()
        self.delete_button = tk.Button(self.deleteTab, text="Delete", command=self.delete)
        self.delete_button.pack()
        self.delete_status_label = tk.Label(self.deleteTab, text="")
        self.delete_status_label.pack()

        # Tree Tab
        self.treeTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.treeTab, text='Tree')
        self.tree_display = ttk.Treeview(self.treeTab)
        self.tree_display.pack(expand=1, fill="both")
        
        self.tree_button = tk.Button(self.treeTab, text="Display Tree", command=self.display_tree)
        self.tree_button.pack()

        # Owners Tab
        self.ownersTab = ttk.Frame(self.tabControl)
        self.tabControl.add(self.ownersTab, text='Owners')
        self.owners_text = tk.Text(self.ownersTab, wrap=tk.WORD)
        self.owners_text.pack()
        self.owners_button = tk.Button(self.ownersTab, text="Find Owners", command=self.find_owners)
        self.owners_button.pack()

        self.tabControl.pack(expand=1, fill="both")

        self.tabControl.bind("<<NotebookTabChanged>>", self.tab_changed)

    def tab_changed(self, event):
        selected_tab_index = self.tabControl.index(self.tabControl.select())
        if selected_tab_index == 0:
            self.current_tab = self.insertTab
        elif selected_tab_index == 1:
            self.current_tab = self.deleteTab
        elif selected_tab_index == 2:
            self.current_tab = self.treeTab
            self.display_tree()
        elif selected_tab_index == 3:
            self.current_tab = self.ownersTab
            self.find_owners()

    def insert(self):
        vin = self.insert_vin_entry.get()
        date = self.insert_date_entry.get()
        owner = self.insert_owner_entry.get()
        car = Car(vin, date, owner)
        self.tree.insert(car)
        self.insert_status_label.config(text="Insertion successful")

    def delete(self):
        vin = self.delete_vin_entry.get()
        try:
            self.tree.delete(vin)
            self.delete_status_label.config(text="Deletion successful")
        except:
            self.delete_status_label.config(text="VIN not found")

    def display(self):
        self.tree.display_text = ""
        self.tree.display()
        self.display_text.delete(1.0, tk.END)
        self.display_text.insert(tk.END, self.tree.display_text)

    def display_tree(self):
        self.tree_display.delete(*self.tree_display.get_children())
        self._display_tree(self.tree)

    def _display_tree(self, node, parent=''):
        if node.key is not None:
            current_node = self.tree_display.insert(parent, 'end', text=repr(node.key))
            if node.hasLeft():
                self._display_tree(node.leftChild, parent=current_node)
            if node.hasRight():
                self._display_tree(node.rightChild, parent=current_node)

    def find_owners(self):
        owners = self.tree.find_owners_with_multiple_cars()
        self.owners_text.delete(1.0, tk.END)
        self.owners_text.insert(tk.END, "\n".join(owners))



def main():
    tree = BinaryTree()
    tree.insert(Car("ABC123", "2023-07-20", "Іванов Іван Іванович"))
    tree.insert(Car("DEF456", "2023-08-01", "Петров Петро Петрович"))
    tree.insert(Car("GHI789", "2023-09-01", "Сидоров Сидір Сидорович"))
    tree.insert(Car("ABC452", "2023-10-01", "Петров Петро Петрович"))
    tree.insert(Car("GHI780", "2023-09-01", "Сидоров Сидір Сидорович"))
    tree.insert(Car("ABC451", "2023-10-01", "Петров Петро Петрович"))
    tree.insert(Car("GHI782", "2023-09-01", "Сидоров Сидір Сидорович"))

    root = tk.Tk()
    app = BinaryTreeUI(root, tree)
    root.mainloop()

if __name__ == "__main__":
    main()
