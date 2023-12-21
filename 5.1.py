import tkinter as tk
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = {}

    def add_edge(self, start, end, weight):
        if start in self.graph:
            self.graph[start].append((end, weight))
        else:
            self.graph[start] = [(end, weight)]

    def find_paths(self, start, end, target_value):
        result_paths = []

        def dfs(current_vertex, current_sum, path):
            if current_vertex == end and current_sum == target_value:
                result_paths.append(path.copy())

            for neighbor, weight in self.graph.get(current_vertex, []):
                if neighbor not in path:
                    dfs(neighbor, current_sum + weight, path + [neighbor])

        dfs(start, 0, [start])
        return result_paths


class GraphUI:
    def __init__(self, master):
        self.master = master
        master.title("Graph Path Finder")

        self.graph = Graph()
        self.graph.add_edge('A', 'B', 2)
        self.graph.add_edge('A', 'C', 3)
        self.graph.add_edge('B', 'D', 1)
        self.graph.add_edge('C', 'D', 5)
        self.graph.add_edge('D', 'E', -4)
        self.graph.add_edge('A', 'E', 6)

        self.label_start = tk.Label(master, text="Start Vertex:")
        self.label_start.grid(row=0, column=0, padx=10, pady=10)
        self.entry_start = tk.Entry(master)
        self.entry_start.insert(0, "A")
        self.entry_start.grid(row=0, column=1, padx=10, pady=10)

        self.label_end = tk.Label(master, text="End Vertex:")
        self.label_end.grid(row=1, column=0, padx=10, pady=10)
        self.entry_end = tk.Entry(master)
        self.entry_end.insert(0, "E")
        self.entry_end.grid(row=1, column=1, padx=10, pady=10)

        self.label_target = tk.Label(master, text="Target Value:")
        self.label_target.grid(row=2, column=0, padx=10, pady=10)
        self.entry_target = tk.Entry(master)
        self.entry_target.insert(0, 4)
        self.entry_target.grid(row=2, column=1, padx=10, pady=10)

        self.button_find_paths = tk.Button(
            master, text="Find Paths", command=self.find_paths)
        self.button_find_paths.grid(row=3, column=0, columnspan=2, pady=10)

        self.text_result = tk.Text(master, height=10, width=40)
        self.text_result.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        self.graph_visualization = nx.Graph()
        self.visualize_graph()

    def find_paths(self):
        start_vertex = self.entry_start.get()
        end_vertex = self.entry_end.get()
        target_value = int(self.entry_target.get())

        paths = self.graph.find_paths(start_vertex, end_vertex, target_value)

        self.text_result.delete(1.0, tk.END)  # Clear previous results

        if paths:
            self.text_result.insert(
                tk.END, f"Paths from {start_vertex} to {end_vertex} with target value {target_value}:\n")
            self.text_result.insert(tk.END, f"{paths[0]}\n")
        else:
            self.text_result.insert(
                tk.END, f"No paths from {start_vertex} to {end_vertex} with target value {target_value} found.")

    def visualize_graph(self):
        for vertex, edges in self.graph.graph.items():
            self.graph_visualization.add_node(vertex)
            for edge, weight in edges:
                self.graph_visualization.add_edge(vertex, edge, weight=weight)

        # Use shell_layout for a linear layout
        pos = nx.shell_layout(self.graph_visualization)

        # Specify arrowstyle and arrowsize for arrows
        edge_labels = {
            (i, j): f"{self.graph_visualization[i][j]['weight']}" for i, j in self.graph_visualization.edges()}
        edge_colors = [self.graph_visualization[i][j]['weight']
                       for i, j in self.graph_visualization.edges()]

        # Draw graph with arrows and weights
        nx.draw(self.graph_visualization, pos, with_labels=True,
                font_weight='bold', node_size=700, node_color='skyblue', edge_color=edge_colors, arrows=True, connectionstyle='arc3,rad=0.1', arrowstyle='->')

        # Add edge labels
        nx.draw_networkx_edge_labels(
            self.graph_visualization, pos, edge_labels=edge_labels)

        plt.title("Graph Visualization")
        plt.show()


if __name__ == "__main__":
    root = tk.Tk()
    gui = GraphUI(root)
    root.mainloop()
