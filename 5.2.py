from collections import defaultdict
import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt


class Graph:
    def __init__(self):
        self.graph = defaultdict(list)

    def add_edge(self, u, v):
        self.graph[u].append(v)
        self.graph[v].append(u)

    def visualize_graph(self):
        # Create an undirected graph for visualization
        self.graph_visualization = nx.Graph()

        for vertex, edges in self.graph.items():
            self.graph_visualization.add_node(vertex)
            for edge in edges:
                self.graph_visualization.add_edge(vertex, edge)

        # Use shell_layout for a linear layout
        pos = nx.shell_layout(self.graph_visualization)

        # Draw graph without arrows and weights
        nx.draw(self.graph_visualization, pos, with_labels=True,
                font_weight='bold', node_size=700, node_color='skyblue', edge_color='gray')

        plt.title("Graph Visualization")
        plt.show()


class GraphUI(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Graph Information")
        self.geometry("400x500")

        self.graph = Graph()

        # Default data
        self.graph.add_edge(1, 2)
        self.graph.add_edge(1, 3)
        self.graph.add_edge(2, 4)
        self.graph.add_edge(2, 5)

        self.create_widgets()

    def create_widgets(self):
        label = ttk.Label(self, text="Graph Information")
        label.pack(pady=10)

        self.graph_text = tk.Text(self, height=8, width=40)
        self.graph_text.pack()

        self.update_graph_text()

        entry_label = ttk.Label(self, text="Enter Edge (e.g., 1 2):")
        entry_label.pack(pady=5)

        self.entry_var = tk.StringVar()
        entry_field = ttk.Entry(self, textvariable=self.entry_var)
        entry_field.pack(pady=5)

        add_edge_button = ttk.Button(
            self, text="Add Edge", command=self.add_edge)
        add_edge_button.pack(pady=5)

        clear_graph_button = ttk.Button(
            self, text="Clear Graph", command=self.clear_graph)
        clear_graph_button.pack(pady=5)

        visualize_graph_button = ttk.Button(
            self, text="Visualize Graph", command=self.visualize_graph)
        visualize_graph_button.pack(pady=5)

        calculate_button = ttk.Button(
            self, text="Calculate Density", command=self.calculate_density)
        calculate_button.pack(pady=10)

        self.result_label = ttk.Label(self, text="")
        self.result_label.pack(pady=10)

    def update_graph_text(self):
        self.graph_text.delete(1.0, tk.END)
        for u, neighbors in self.graph.graph.items():
            self.graph_text.insert(tk.END, f"{u}: {neighbors}\n")

    def add_edge(self):
        edge_input = self.entry_var.get()
        try:
            u, v = map(int, edge_input.split())
            self.graph.add_edge(u, v)
            self.update_graph_text()
            self.entry_var.set("")  # Clear the entry field
        except ValueError:
            tk.messagebox.showerror(
                "Error", "Invalid input. Please enter two integers separated by a space.")

    def clear_graph(self):
        self.graph = Graph()
        self.graph_text.delete(1.0, tk.END)
        self.entry_var.set("")

    def visualize_graph(self):
        self.graph.visualize_graph()

    def calculate_density(self):
        num_vertices = len(self.graph.graph)
        num_edges = sum(len(neighbors)
                        for neighbors in self.graph.graph.values()) // 2

        average_density = self.calculate_average_density()

        result_text = (
            f"Number of vertices: {num_vertices}\n"
            f"Number of edges: {num_edges}\n"
            f"Average density: {average_density:.2f}"
        )

        self.result_label.config(text=result_text)

    def calculate_average_density(self):
        num_vertices = 0
        num_edges = 0

        visited = defaultdict(bool)

        for node in self.graph.graph:
            if not visited[node]:
                vertex_count = [0]
                edge_count = [0]
                self.dfs(node, visited, vertex_count, edge_count)
                num_vertices += vertex_count[0]
                num_edges += edge_count[0] // 2

        if num_vertices == 0:
            return 0

        average_density = num_edges / num_vertices
        return average_density

    def dfs(self, node, visited, vertex_count, edge_count):
        visited[node] = True
        vertex_count[0] += 1

        for neighbor in self.graph.graph[node]:
            edge_count[0] += 1
            if not visited[neighbor]:
                self.dfs(neighbor, visited, vertex_count, edge_count)


if __name__ == "__main__":
    app = GraphUI()
    app.mainloop()
