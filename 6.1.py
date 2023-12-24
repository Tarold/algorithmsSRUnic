import tkinter as tk
from tkinter import ttk, messagebox
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class NetworkGraph:
    def __init__(self):
        self.unique_vertices = set()
        self.num_nodes = 0
        self.edges = []

    def add_edge(self, src, dest, speed, busyness):
        self.unique_vertices.add(src)
        self.unique_vertices.add(dest)
        self.num_nodes = len(self.unique_vertices)

        self.edges.append(
            (src, dest, speed / busyness if (busyness > 1) else speed))
        self.edges.append(
            (dest, src, speed / busyness if (busyness > 1) else speed))

    def calculate_shortest_path_bellman_ford(self, source, destination):
        nodes = list(self.unique_vertices)
        num_nodes = len(nodes)
        weight = {node: float('inf') for node in nodes}
        weight[nodes[source]] = 0
        parent = {node: None for node in nodes}

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
        current_vertex = nodes[destination]
        while current_vertex is not None:
            shortest_path.append(current_vertex)
            current_vertex = parent[current_vertex]

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

    def calculate_all_shortest_paths_floyd_warshall(self):
        num_nodes = self.num_nodes
        dist = [[float('inf')] * num_nodes for _ in range(num_nodes)]
        pred = [[None] * num_nodes for _ in range(num_nodes)]

        # Initialize distances with edge weights and predecessors
        for src, dest, cost in self.edges:
            dist[src][dest] = cost
            pred[src][dest] = src

        for i in range(num_nodes):
            dist[i][i] = 0
            pred[i][i] = None

        # Update distances and predecessors using Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    if dist[i][k] + dist[k][j] < dist[i][j]:
                        dist[i][j] = dist[i][k] + dist[k][j]
                        pred[i][j] = pred[k][j]

        # Extract all shortest paths
        all_shortest_paths = [[[]
                               for _ in range(num_nodes)] for _ in range(num_nodes)]
        for i in range(num_nodes):
            for j in range(num_nodes):
                path = self.construct_shortest_path(i, j, pred)
                all_shortest_paths[i][j] = path

        return dist, all_shortest_paths

    def construct_shortest_path(self, i, j, pred):
        path = []
        while j is not None:
            path.insert(0, j)
            j = pred[i][j]
        return path


class NetworkGraphUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Network Graph UI")

        self.graph = NetworkGraph()
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
            self.master, values=list(range(self.graph.num_nodes)))
        self.from_entry.grid(row=1, column=1, padx=10)
        self.from_entry.set(0)

        self.to_label = tk.Label(self.master, text="To Node:")
        self.to_label.grid(row=1, column=2, padx=10)

        self.to_entry = ttk.Combobox(
            self.master, values=list(range(self.graph.num_nodes)))
        self.to_entry.grid(row=1, column=3, padx=10)
        self.to_entry.set(self.graph.num_nodes - 1)

        self.calculate_button = tk.Button(
            self.master, text="Calculate Shortest Path", command=self.calculate_shortest_path)
        self.calculate_button.grid(row=2, column=0, columnspan=4, pady=10)

        self.result_label = tk.Label(self.master, text="")
        self.result_label.grid(row=3, column=0, columnspan=4)

        self.edge_entry_label = tk.Label(
            self.master, text="Enter Edge (src, dest, speed, busyness):")
        self.edge_entry_label.grid(
            row=6, column=0, columnspan=2, pady=5, padx=10)

        self.edge_entry = ttk.Entry(self.master)
        self.edge_entry.grid(row=6, column=2, padx=10)

        self.add_edge_button = tk.Button(
            self.master, text="Add Edge", command=self.add_edge)
        self.add_edge_button.grid(row=6, column=3, padx=10)

        self.default_graph_button = tk.Button(
            self.master, text="Load Default Graph", command=self.load_default_graph)
        self.default_graph_button.grid(
            row=7, column=0, columnspan=2, pady=5, padx=10)

        self.clear_graph_button = tk.Button(
            self.master, text="Clear Graph", command=self.clear_graph)
        self.clear_graph_button.grid(
            row=7, column=2, columnspan=2, pady=5, padx=10)

        self.show_all_paths_button = tk.Button(
            self.master, text="Show All Shortest Paths", command=self.show_all_shortest_paths)
        self.show_all_paths_button.grid(
            row=8, column=0, columnspan=4, pady=10)

    def show_all_shortest_paths(self):
        try:
            all_dist, all_shortest_paths = self.graph.calculate_all_shortest_paths_floyd_warshall()

            if not all_shortest_paths:
                result_str = "No shortest paths found."
            else:
                result_str = "All Shortest Paths:\n"
                for i in range(0, len(all_shortest_paths)):
                    for j in range(0, len(all_shortest_paths[0])):
                        result_str += f"From {i} to {j}: {all_shortest_paths[i][j]}, Distance: {all_dist[i][j]}\n"

            messagebox.showinfo("All Shortest Paths", result_str)

        except ValueError as e:
            messagebox.showerror("Error", f"Error: {e}")

    def add_edge(self):
        try:
            edge_values = list(map(float, self.edge_entry.get().split(',')))
            if len(edge_values) != 4:
                raise ValueError(
                    "Invalid edge format. Please enter (src, dest, speed, busyness).")

            src, dest, speed, busyness = edge_values
            self.graph.add_edge(int(src), int(dest), speed, busyness)

            self.edge_entry.delete(0, tk.END)  # Clear the entry
            self.create_graph_visualization()

        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {e}")

    def load_default_graph(self):
        self.graph = NetworkGraph()
        # Add default edges
        default_edges = [(0, 1, 5, 1.2), (0, 2, 3, 0.5), (1, 3, 6, 1.5),
                         (2, 1, 1, 0.7), (2, 4, 2, 1), (3, 5, 1, 1), (4, 5, 3, 1.1)]
        for edge in default_edges:
            self.graph.add_edge(*edge)

        self.create_graph_visualization()

    def clear_graph(self):
        self.graph = NetworkGraph()
        self.create_graph_visualization()

    def create_graph_visualization(self):
        self.update_combobox_values()
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
        edge_labels = {}  # New dictionary for edge labels

        for edge in self.graph.edges:
            src, dest, weight = edge
            G.add_edge(src, dest, weight=weight)
            edge_labels[(src, dest)] = f"{weight:.2f}"

        pos = nx.spring_layout(G)
        nx.draw(G, pos, with_labels=True, ax=self.graph_ax, node_size=700, node_color="skyblue",
                font_size=8, font_color="black", font_weight="bold", arrowsize=10)

        # Draw edge labels
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=self.graph_ax, font_color="red")

    def calculate_shortest_path(self):
        source = int(self.from_entry.get())
        destination = int(self.to_entry.get())

        try:
            shortest_path = self.graph.calculate_shortest_path_bellman_ford(
                source, destination)
            distanceMatrix = self.graph.calculate_all_shortest_paths_floyd_warshall()
            distance = distanceMatrix[
                source][destination]

            result_str = f"Shortest Path: {shortest_path}\nDistance: {distance}"
        except ValueError as e:
            result_str = f"Error: {e}"

        self.result_label.config(text=result_str)

    def update_combobox_values(self):
        nodes = list(self.graph.unique_vertices)
        self.from_entry['values'] = nodes
        self.to_entry['values'] = nodes


if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkGraphUI(root)
    root.mainloop()
