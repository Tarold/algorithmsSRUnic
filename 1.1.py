import tkinter as tk
from tkinter import ttk, simpledialog
from timeit import default_timer as timer

class Node: 
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

class DoubleLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_to_beginning(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node
        return f"Added {data} to the beginning."

    def add_after(self, prev_node_data, data):
        prev_node = self.find_node(prev_node_data)
        if prev_node:
            new_node = Node(data)
            new_node.prev = prev_node
            new_node.next = prev_node.next
            prev_node.next = new_node
            if new_node.next:
                new_node.next.prev = new_node
            else:
                self.tail = new_node
            return f"Added {data} after {prev_node_data}."
        else:
            return f"Node with data {prev_node_data} not found."

    def find_node(self, data):
        current = self.head
        while current:
            if current.data == data:
                return current
            current = current.next
        return None

    def delete_node(self, data):
        node = self.find_node(data)
        if node:
            if node.prev:
                node.prev.next = node.next
            else:
                self.head = node.next
            if node.next:
                node.next.prev = node.prev
            else:
                self.tail = node.prev
            return f"Deleted node with data {data}."
        else:
            return f"Node with data {data} not found."

    def display_from_start(self):
        result = []
        current = self.head
        while current:
            result.append(current.data)
            current = current.next
        return result

    def display_from_end(self):
        result = []
        current = self.tail
        while current:
            result.append(current.data)
            current = current.prev
        return result

class PriorityQueue:
    def __init__(self):
        self.heap = []

    def insert(self, item):
        self.heap.append(item)
        self.heapify_up(len(self.heap) - 1)
        return f"Inserted {item} into the priority queue."

    def remove(self):
        if not self.heap:
            return "Priority queue is empty."
        if len(self.heap) == 1:
            return self.heap.pop()
        root = self.heap[0]
        self.heap[0] = self.heap.pop()
        self.heapify_down()
        return root

    def heapify_up(self, index):
        while index > 0:
            parent_index = (index - 1) // 2
            if self.heap[index] < self.heap[parent_index]:
                self.heap[index], self.heap[parent_index] = self.heap[parent_index], self.heap[index]
                index = parent_index
            else:
                break

    def heapify_down(self, index=0):
        left_child_index = 2 * index + 1
        right_child_index = 2 * index + 2
        smallest_index = index

        if left_child_index < len(self.heap) and self.heap[left_child_index] < self.heap[smallest_index]:
            smallest_index = left_child_index
        if right_child_index < len(self.heap) and self.heap[right_child_index] < self.heap[smallest_index]:
            smallest_index = right_child_index

        if smallest_index != index:
            self.heap[index], self.heap[smallest_index] = self.heap[smallest_index], self.heap[index]
            self.heapify_down(smallest_index)

    def build_heap(self, arr):
        self.heap = arr
        for i in range(len(arr) // 2, -1, -1):
            self.heapify_down(i)
        return "Built heap from array."

    def sort(self):
        heapOld = list(self.heap)
        sorted_arr = []
        while True:
            item = self.remove()
            if item == 'Priority queue is empty.':
                break
            sorted_arr.append(item)
        self.heap = heapOld
        return sorted_arr

    def display(self):
        return self.heap

def bubble_sort(arr):
    n = len(arr)
    for i in range(n - 1):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]

class VisualApp:
    
    def __init__(self, root):
        self.root = root
        self.root.title("Visual App")

        self.linked_list = DoubleLinkedList()
        self.priority_queue = PriorityQueue()
        self.create_widgets()

    def create_widgets(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(pady=10, padx=10)

        tab1 = ttk.Frame(notebook)
        tab2 = ttk.Frame(notebook)
        tab3 = ttk.Frame(notebook)

        notebook.add(tab1, text="Double Linked List")
        notebook.add(tab2, text="Priority Queue")
        notebook.add(tab3, text="Sorting Speed Comparison")

        self.create_linked_list_tab(tab1)

        self.create_priority_queue_tab(tab2)

        self.create_timer_tab(tab3)

    def create_linked_list_tab(self, tab):
        linked_list_label = ttk.Label(tab, text="Double Linked List:")
        linked_list_label.pack()

        insert_default_button = ttk.Button(tab, text="Insert Default", command=self.insert_default_linked_list)
        insert_default_button.pack()

        add_to_beginning_button = ttk.Button(tab, text="Add to Beginning", command=self.add_to_beginning)
        add_to_beginning_button.pack()

        add_after_button = ttk.Button(tab, text="Add After", command=self.add_after)
        add_after_button.pack()

        delete_node_button = ttk.Button(tab, text="Delete Node", command=self.delete_node)
        delete_node_button.pack()

        display_label = ttk.Label(tab, text="Display from start:")
        display_label.pack()

        self.display_text_start = tk.Text(tab, height=2, width=30)
        self.display_text_start.pack()

        display_label_end = ttk.Label(tab, text="Display from end:")
        display_label_end.pack()

        self.display_text_end = tk.Text(tab, height=2, width=30)
        self.display_text_end.pack()

    def create_priority_queue_tab(self, tab):
        priority_queue_label = ttk.Label(tab, text="Priority Queue:")
        priority_queue_label.pack()

        insert_default_button = ttk.Button(tab, text="Insert Default", command=self.insert_default_priority_queue)
        insert_default_button.pack()

        insert_button = ttk.Button(tab, text="Insert", command=self.insert)
        insert_button.pack()

        remove_button = ttk.Button(tab, text="Remove first", command=self.remove)
        remove_button.pack()

        build_heap_button = ttk.Button(tab, text="Insert Heap", command=self.build_heap)
        build_heap_button.pack()

        sort_button = ttk.Button(tab, text="Sort", command=self.sort)
        sort_button.pack()

        display_label = ttk.Label(tab, text="Display:")
        display_label.pack()

        self.display_text_priority_queue = tk.Text(tab, height=4, width=50)
        self.display_text_priority_queue.pack()

    def create_timer_tab(self, tab3):
        comparison_label = ttk.Label(tab3, text="Sorting Speed Comparison:")
        comparison_label.pack()

        compare_speed_button = ttk.Button(tab3, text="Compare Sorting Speed", command=self.compare_sorting_speed)
        compare_speed_button.pack()

        self.display_text_comparison = tk.Text(tab3, height=5, width=50)
        self.display_text_comparison.pack()
    
    def compare_sorting_speed(self):
        arr = [9, 7, 5, 2, 3, 4, 6, 8, 10, 1, 
               9, 7, 5, 2, 3, 4, 6, 8, 10, 1, 
               7, 5, 2, 3, 4, 6, 8, 10, 
               15, 23, 17, 12, 19, 21, 14, 16, 18, 20, 
               25, 27, 35, 32, 30, 28, 31, 29, 
               45, 42, 40, 38, 41, 39, 50, 
               55, 53, 49, 47, 48, 46, 51, 52, 
               60, 58, 57, 56, 54, 59, 
               70, 68, 65, 63, 64, 66, 69, 
               80, 78, 75, 72, 74, 76, 79, 
               90, 88, 85, 83, 84, 86, 89, 
               95, 92, 98, 96, 93, 97, 99, 100]

        start_time_heap = timer()
        self.priority_queue.build_heap(arr.copy())
        end_time_heap = timer()

        start_time_bubble = timer() 
        bubble_sort(arr.copy())
        end_time_bubble = timer() 

        display_text = f"Heap Sort Time: {((end_time_heap - start_time_heap) * 1000):.6f} milliseconds\n"
        display_text += f"Bubble Sort Time: {((end_time_bubble - start_time_bubble) * 1000):.6f} milliseconds"

        self.display_text_comparison.delete(1.0, tk.END)
        self.display_text_comparison.insert(tk.END, display_text)

    def insert_default_linked_list(self):
        self.linked_list.add_to_beginning(4)
        self.linked_list.add_to_beginning(3)
        self.linked_list.add_to_beginning(2)
        self.linked_list.add_to_beginning(1)
        self.update_display_linked_list('Add Default data [1, 2, 3, 4]')

    def insert_default_priority_queue(self):
        arr = [9, 7, 5, 2, 3, 4, 6, 8, 10, 1, 9, 7, 5, 2, 3, 4, 6, 8, 10, 1, 7, 5, 2, 3, 4, 6, 8, 10]
        for item in arr:
            self.priority_queue.insert(item)
        self.update_display_priority_queue('Add Default data')

    def update_display_linked_list(self, result):
        self.display_text_start.delete(1.0, tk.END)
        self.display_text_start.insert(tk.END, f"Original: {str(self.linked_list.display_from_start())}\nOperation result: {result}")
        self.display_text_end.delete(1.0, tk.END)
        self.display_text_end.insert(tk.END, f"Original: {str(self.linked_list.display_from_end())}\nOperation result: {result}")

    def add_to_beginning(self):
        data = simpledialog.askinteger("Add to Beginning", "Enter data to add to the beginning:")
        result = self.linked_list.add_to_beginning(data)
        self.update_display_linked_list(result)

    def add_after(self):
        prev_node_data = simpledialog.askinteger("Add After", "Enter data of the previous node:")
        data = simpledialog.askinteger("Add After", f"Enter data to add after {prev_node_data}:")
        result = self.linked_list.add_after(prev_node_data, data)
        self.update_display_linked_list(result)

    def delete_node(self):
        data = simpledialog.askinteger("Delete Node", "Enter data to delete:")
        result = self.linked_list.delete_node(data)
        self.update_display_linked_list(result)

    def insert(self):
        data = simpledialog.askinteger("Insert", "Enter data to insert:")
        result = self.priority_queue.insert(data)
        self.update_display_priority_queue(result)

    def remove(self):
        result = self.priority_queue.remove()
        self.update_display_priority_queue(f"Removed {result} from the priority queue.")

    def build_heap(self):
        data = tk.simpledialog.askstring("Build Heap", "Enter a comma-separated array to build the heap:")
        arr = list(map(int, data.split(',')))
        result = self.priority_queue.build_heap(arr)
        self.update_display_priority_queue(result)

    def sort(self):
        result = self.priority_queue.sort()
        self.update_display_priority_queue(result)

    def update_display_priority_queue(self, result):
        self.display_text_priority_queue.delete(1.0, tk.END)
        self.display_text_priority_queue.insert(tk.END, f"Original: {str(self.priority_queue.display())}\nOperation result: {result}")

if __name__ == "__main__":
    root = tk.Tk()
    app = VisualApp(root)
    root.mainloop()
