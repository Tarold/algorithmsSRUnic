import tkinter as tk
from tkinter import ttk
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class NetworkGraph:
    def __init__(self, num_nodes):
        self.num_nodes = num_nodes
        self.edges = []

    def add_edge(self, src, dest, speed, busyness):
        self.edges.append(
            (src, dest, speed / busyness if (busyness > 1) else speed))
        self.edges.append(
            (dest, src, speed / busyness if (busyness > 1) else speed))

    def calculate_shortest_path_bellman_ford(self, source, destination):
        num_nodes = self.num_nodes
        weight = [float('inf')] * num_nodes
        weight[source] = 0
        parent = [-1] * num_nodes

        # Bellman-Ford algorithm
        for _ in range(num_nodes - 1):
            for src, dest, cost in self.edges:
                if weight[src] != float('inf') and weight[src] + cost < weight[dest]:
                    weight[dest] = weight[src] + cost
                    parent[dest] = src

        # Check for negative weight cycles
        for src, dest, cost in self.edges:
            if weight[src] != float('inf') and weight[src] + cost < weight[dest]:
                raise ValueError("Graph contains a negative weight cycle")

        shortest_path = []
        while destination != -1:
            shortest_path.append(destination)
            destination = parent[destination]
        shortest_path.reverse()

        return shortest_path

    def calculate_all_shortest_paths_floyd_warshall(self):
        num_nodes = self.num_nodes
        dist = [[float('inf')]*num_nodes for _ in range(num_nodes)]

        # Initialize distances with edge weights
        for src, dest, cost in self.edges:
            dist[src][dest] = cost

        for i in range(num_nodes):
            dist[i][i] = 0

        # Update distances using Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist


class NetworkGraphUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Network Graph UI")

        self.num_nodes = 6
        self.graph = NetworkGraph(self.num_nodes)
        self.graph.add_edge(0, 1, 5, 1.2)
        self.graph.add_edge(0, 2, 3, 0.5)
        self.graph.add_edge(1, 3, 6, 1.5)
        self.graph.add_edge(2, 1, 1, 0.7)
        self.graph.add_edge(2, 4, 2, 1)
        self.graph.add_edge(3, 5, 1, 1)
        self.graph.add_edge(4, 5, 3, 1.1)
        self.create_widgets()
        self.create_graph_visualization()

    def create_widgets(self):
        self.label = tk.Label(self.master, text="Shortest Path Calculation")
        self.label.grid(row=0, column=0, columnspan=3, pady=10)

        self.from_label = tk.Label(self.master, text="From Node:")
        self.from_label.grid(row=1, column=0, padx=10)

        self.from_entry = ttk.Combobox(
            self.master, values=list(range(self.num_nodes)))
        self.from_entry.grid(row=1, column=1, padx=10)
        self.from_entry.set(0)

        self.to_label = tk.Label(self.master, text="To Node:")
        self.to_label.grid(row=1, column=2, padx=10)

        self.to_entry = ttk.Combobox(
            self.master, values=list(range(self.num_nodes)))
        self.to_entry.grid(row=1, column=3, padx=10)
        self.to_entry.set(self.num_nodes - 1)

        self.calculate_button = tk.Button(
            self.master, text="Calculate Shortest Path", command=self.calculate_shortest_path)
        self.calculate_button.grid(row=2, column=0, columnspan=4, pady=10)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=3, column=0, columnspan=4)

    def create_graph_visualization(self):
        self.graph_visualization_frame = ttk.Frame(self.master)
        self.graph_visualization_frame.grid(
            row=4, column=0, columnspan=4, pady=10)

        self.graph_fig, self.graph_ax = plt.subplots()
        self.draw_graph()
        self.graph_canvas = FigureCanvasTkAgg(
            self.graph_fig, master=self.graph_visualization_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def draw_graph(self):
        G = nx.DiGraph()
        for edge in self.graph.edges:
            src, dest, _ = edge
            G.add_edge(src, dest)

        # You can choose a different layout if needed
        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=self.graph_ax, node_size=700, node_color="skyblue",
                font_size=8, font_color="black", font_weight="bold", arrowsize=10)

    def calculate_shortest_path(self):
        source = int(self.from_entry.get())
        destination = int(self.to_entry.get())

        try:
            shortest_path = self.graph.calculate_shortest_path_bellman_ford(
                source, destination)
            distance = self.graph.calculate_all_shortest_paths_floyd_warshall()[
                source][destination]

            result_str = f"Shortest Path: {shortest_path}\nDistance: {distance}"
        except ValueError as e:
            result_str = f"Error: {e}"

        self.result_label.config(text=result_str)
        self.draw_graph()
        self.graph_canvas.draw()


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkGraphUI(root)
    root.mainloop()
