import tkinter as tk
from tkinter import ttk, simpledialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import networkx as nx
import tkinter.font as tkFont


class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, value):
        self.nodes.add(value)
        self.edges[value] = []

    def add_edge(self, from_node, to_node, weight=None, is_blocked=False, **kwargs):
        if from_node not in self.nodes:
            self.add_node(from_node)
        if to_node not in self.nodes:
            self.add_node(to_node)

        edge_exists = any(to == to_node for to, _, _,
                          _ in self.edges[from_node])
        if edge_exists:
            for i, (to, w, blocked, _) in enumerate(self.edges[from_node]):
                if to == to_node:
                    if weight is not None or is_blocked is not None:
                        # Update existing edge with new data
                        self.edges[from_node][i] = (
                            to_node, weight if weight is not None else w, is_blocked if is_blocked is not None else blocked, kwargs)
                        self.edges[to_node][i] = (
                            from_node, weight if weight is not None else w, is_blocked if is_blocked is not None else blocked, kwargs)
                    break
        else:
            self.edges[from_node].append((to_node, weight, is_blocked, kwargs))
            self.edges[to_node].append((from_node, weight, is_blocked, kwargs))

    def calculate_all_shortest_paths_floyd_warshall(self):
        num_nodes = len(self.nodes)
        node_indices = {node: index for index, node in enumerate(self.nodes)}
        dist = [[float('inf')]*num_nodes for _ in range(num_nodes)]
        print(node_indices)
        # Initialize distances with edge weights
        for node, neighbors in self.edges.items():
            for neighbor, weight, _, _ in neighbors:
                # Assuming a default cost of 1 for unweighted edges
                dist[node_indices[node]][node_indices[neighbor]] = 1

        for i in range(num_nodes):
            dist[i][i] = 0

        # Update distances using Floyd-Warshall algorithm
        for k in range(num_nodes):
            for i in range(num_nodes):
                for j in range(num_nodes):
                    dist[i][j] = min(dist[i][j], dist[i][k] + dist[k][j])

        return dist


def dijkstra(graph, source, target):
    distances = {node: float('infinity') for node in graph.nodes}
    distances[source] = 0

    unvisited_nodes = set(graph.nodes)

    while unvisited_nodes:
        current_node = min(unvisited_nodes, key=lambda node: distances[node])
        unvisited_nodes.remove(current_node)

        for neighbor, weight, is_blocked, _ in graph.edges[current_node]:
            if not is_blocked:
                potential_distance = distances[current_node] + weight
                if potential_distance < distances[neighbor]:
                    distances[neighbor] = potential_distance

    return distances[target]


class GraphUI:
    def __init__(self, master, graph):
        self.master = master
        self.graph = graph
        self.source_var = tk.StringVar()
        self.target_var = tk.StringVar()

        self.master.title("Graph UI")

        self.create_widgets()
        self.create_graph_visualization()

    def create_widgets(self):
        frame = ttk.Frame(self.master, padding="10")
        frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(frame, text="Source Node:").grid(
            row=0, column=0, sticky=tk.W)
        self.source_combobox = ttk.Combobox(
            frame, textvariable=self.source_var, values=list(self.graph.nodes))
        self.source_combobox.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(frame, text="Target Node:").grid(
            row=1, column=0, sticky=tk.W)
        self.target_combobox = ttk.Combobox(
            frame, textvariable=self.target_var, values=list(self.graph.nodes))
        self.target_combobox.grid(row=1, column=1, padx=5, pady=5)

        calculate_button = ttk.Button(
            frame, text="Calculate Shortest Path", command=self.calculate_shortest_path)
        calculate_button.grid(row=2, column=0, columnspan=2, pady=10)

        visualize_button = ttk.Button(
            frame, text="Visualize Graph", command=self.update_graph_visualization)
        visualize_button.grid(row=3, column=0, columnspan=2, pady=10)

        add_edge_button = ttk.Button(
            frame, text="Add Edge", command=self.add_edge)
        add_edge_button.grid(row=4, column=0, columnspan=2, pady=10)

        remove_graph_button = ttk.Button(
            frame, text="Remove Graph", command=self.remove_graph)
        remove_graph_button.grid(row=5, column=0, columnspan=2, pady=10)

        floyd_warshall_button = ttk.Button(
            frame, text="Floyd-Warshall", command=self.calculate_floyd_warshall)
        floyd_warshall_button.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_floyd_warshall(self):
        all_shortest_paths = self.graph.calculate_all_shortest_paths_floyd_warshall()
        column_names = list(self.graph.nodes)

        # Create a new window to display the result
        result_window = tk.Toplevel(self.master)
        result_window.title("Floyd-Warshall Result")

        # Create a Treeview widget to display the result in a tabular format
        tree = ttk.Treeview(
            result_window, columns=column_names, show="headings")

        for col in column_names:
            tree.heading(col, text=col)
            # Set column width based on content
            tree.column(col, width=tkFont.Font().measure(
                col) + 10)  # Adjust the padding as needed
            # Center-align the text
            tree.column(col, anchor="center")

        # Add data to the Treeview
        for i, row in enumerate(all_shortest_paths):
            tree.insert("", i, values=row)

        tree.pack()

    def remove_graph(self):
        self.graph.nodes.clear()
        self.graph.edges.clear()

        self.update_graph_visualization()

    def create_graph_visualization(self):
        self.graph_visualization_frame = ttk.Frame(self.master)
        self.graph_visualization_frame.grid(
            row=5, column=0, columnspan=4, pady=10)

        self.graph_fig, self.graph_ax = plt.subplots()
        self.draw_graph()
        self.graph_canvas = FigureCanvasTkAgg(
            self.graph_fig, master=self.graph_visualization_frame)
        self.graph_canvas.draw()
        self.graph_canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

    def update_graph_visualization(self):
        self.graph_fig.clf()
        self.graph_ax = self.graph_fig.add_subplot(111)
        self.draw_graph()
        self.graph_canvas.draw()
        self.update_combobox_values()

    def update_combobox_values(self):
        source_values = list(self.graph.nodes)
        target_values = list(self.graph.nodes)

        self.source_combobox['values'] = source_values
        self.target_combobox['values'] = target_values

    def draw_graph(self):
        G = nx.Graph()  # Assuming an undirected graph
        edge_labels = {}

        for node in self.graph.nodes:
            G.add_node(node)

        for from_node, to_nodes in self.graph.edges.items():
            for to_node, weight, is_blocked, _ in to_nodes:
                G.add_edge(from_node, to_node, weight=weight,
                           is_blocked=is_blocked)
                edge_labels[(from_node, to_node)] = f"{weight:.2f}"

        pos = nx.spring_layout(G)

        blocked_edges = [(from_node, to_node) for from_node,
                         to_node, _ in G.edges(data='is_blocked') if _]

        nx.draw(G, pos, with_labels=True, ax=self.graph_ax, node_size=700, node_color="skyblue",
                font_size=8, font_color="black", font_weight="bold", arrowsize=10)

        # Draw blocked edges with a different color
        nx.draw_networkx_edges(
            G, pos, edgelist=blocked_edges, edge_color='red', ax=self.graph_ax)

        # Draw edge labels
        nx.draw_networkx_edge_labels(
            G, pos, edge_labels=edge_labels, ax=self.graph_ax, font_color="black")

    def calculate_shortest_path(self):
        source_node = self.source_var.get()
        target_node = self.target_var.get()

        if source_node and target_node:
            shortest_path_length = dijkstra(
                self.graph, source_node, target_node)
            result_label = ttk.Label(
                self.master, text=f"The shortest path length from {source_node} to {target_node} is: {shortest_path_length}")
            result_label.grid(row=1, column=0, pady=10)

    def add_edge(self):
        source_node = simpledialog.askstring("Add Edge", "Enter source node:")
        target_node = simpledialog.askstring("Add Edge", "Enter target node:")
        weight = simpledialog.askfloat("Add Edge", "Enter edge weight:")
        is_blocked = simpledialog.askinteger(
            "Add Edge", "Enter 1 if the edge is blocked, 0 otherwise:")

        if source_node and target_node and weight is not None and is_blocked is not None:
            self.graph.add_edge(source_node, target_node,
                                weight, is_blocked=bool(is_blocked))
            self.update_graph_visualization()


if __name__ == "__main__":
    root = tk.Tk()

    # Створюємо граф
    network = Graph()

    # Додаємо вузли і зв'язки з вагами (часом пересилання)
    network.add_node('S1')
    network.add_node('R1')
    network.add_node('R2')
    network.add_node('R3')
    network.add_node('R4')
    network.add_node('C1')
    network.add_node('C2')

    network.add_edge('S1', 'R1', 2)
    network.add_edge('R1', 'R2', 1)
    network.add_edge('R1', 'R3', 3, True)
    network.add_edge('R2', 'C1', 2)
    network.add_edge('R2', 'R4', 1)
    network.add_edge('R3', 'R4', 2)
    network.add_edge('R4', 'C2', 3)

    # Створюємо інтерфейс користувача
    graph_ui = GraphUI(root, network)

    root.mainloop()
