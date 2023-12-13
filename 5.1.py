import tkinter as tk
class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end, weight):
        if start not in self.graph:
            self.graph[start] = []
        self.graph[start].append((end, weight))

    def find_paths(self, start, end, target_value):
        visited = set()
        path = []
        result_paths = []

        def dfs(current_vertex, current_sum):
            visited.add(current_vertex)
            path.append(current_vertex)

            if current_vertex == end and current_sum == target_value:
                result_paths.append(path.copy())

            for neighbor, weight in self.graph.get(current_vertex, []): 
                if neighbor not in visited:
                    dfs(neighbor, current_sum + weight)

            visited.remove(current_vertex)
            path.pop()

        dfs(start, 0)
        return result_paths

class GraphUI:
    def __init__(self, master):
        self.master = master
        master.title("Graph Path Finder")

        self.graph = Graph()

        self.label_start = tk.Label(master, text="Start Vertex:")
        self.label_start.grid(row=0, column=0, padx=10, pady=10)
        self.entry_start = tk.Entry(master)
        self.entry_start.grid(row=0, column=1, padx=10, pady=10)

        self.label_end = tk.Label(master, text="End Vertex:")
        self.label_end.grid(row=1, column=0, padx=10, pady=10)
        self.entry_end = tk.Entry(master)
        self.entry_end.grid(row=1, column=1, padx=10, pady=10)

        self.label_target = tk.Label(master, text="Target Value:")
        self.label_target.grid(row=2, column=0, padx=10, pady=10)
        self.entry_target = tk.Entry(master)
        self.entry_target.grid(row=2, column=1, padx=10, pady=10)

        self.button_find_paths = tk.Button(master, text="Find Paths", command=self.find_paths)
        self.button_find_paths.grid(row=3, column=0, columnspan=2, pady=10)

        self.text_result = tk.Text(master, height=10, width=40)
        self.text_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

    def find_paths(self):
        start_vertex = self.entry_start.get()
        end_vertex = self.entry_end.get()
        target_value = int(self.entry_target.get())
        self.graph.add_edge('A', 'B', 2)
        self.graph.add_edge('A', 'C', 3)
        self.graph.add_edge('B', 'D', 1)
        self.graph.add_edge('C', 'D', 5)
        self.graph.add_edge('D', 'E', -4)
        self.graph.add_edge('A', 'E', 6)
        paths = self.graph.find_paths(start_vertex, end_vertex, target_value)

        self.text_result.delete(1.0, tk.END)  # Clear previous results
        
        if paths:
            self.text_result.insert(tk.END, f"Paths from {start_vertex} to {end_vertex} with target value {target_value}:\n")
            for path in paths:
                self.text_result.insert(tk.END, f"{path}\n")
        else:
            self.text_result.insert(tk.END, f"No paths found from {start_vertex} to {end_vertex} with target value {target_value}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphUI(root)
    root.mainloop()
