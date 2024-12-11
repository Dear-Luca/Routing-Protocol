import tkinter as tk
import math
from network import Network
from graphs import adjacency_matrices

class GUI:
    def __init__(self) -> None:
        # create the main window
        self.root = tk.Tk()
        self.root.title("Routing Protocol")

        # current selected matrix
        self.selected_matrix = tk.StringVar(value="Matrix 1")
        self.adj_matrix = adjacency_matrices[self.selected_matrix.get()]

        # network object
        self.network = Network(self.adj_matrix)

        # menu for selecting matrix
        tk.Label(self.root, text="Select Matrix:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.matrix_dropdown = tk.OptionMenu(self.root, self.selected_matrix, *adjacency_matrices.keys(), command=self.update_matrix)
        self.matrix_dropdown.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # canvas for the graph
        self.canvas = tk.Canvas(self.root, width=1200, height=800, bg="white")
        self.canvas.grid(row=1, column=0, columnspan=3)

        # canvas for the scrollable tables
        self.scroll_canvas = tk.Canvas(self.root, width=400, height=800)
        self.scrollbar = tk.Scrollbar(self.root, orient="vertical", command=self.scroll_canvas.yview)
        self.scroll_canvas.configure(yscrollcommand=self.scrollbar.set)

        # positioning scrollable canvas
        self.scroll_canvas.grid(row=1, column=3, sticky="nsew")
        self.scrollbar.grid(row=1, column=4, sticky="ns")

        # Frame for the tables (inside the canvas)
        self.tables_frame = tk.Frame(self.scroll_canvas)
        self.scroll_canvas.create_window((0, 0), window=self.tables_frame, anchor="nw")

        # Configuration for resizing the canvas
        self.tables_frame.bind("<Configure>", lambda e: self.scroll_canvas.configure(scrollregion=self.scroll_canvas.bbox("all")))

        # Button to manually update the tables
        self.update_button = tk.Button(self.root, text="Update Tables", command=lambda: (self.network.update_tables(), self.update_tables()))
        self.update_button.grid(row=2, column=0, pady=10, padx=20)

        self.update_graph_and_tables()

    def update_matrix(self, selection):
        #Update the selected matrix and recalculate network and graph.
        self.adj_matrix = adjacency_matrices[selection]
        self.network = Network(self.adj_matrix)
        self.update_graph_and_tables()

    def update_graph_and_tables(self):
        #Update both the graph and the tables.
        self.canvas.delete("all")  
        self.update_tables()       
        self.draw_graph()         

    def draw_graph(self):
        matrix = self.adj_matrix
        num_nodes = len(matrix)
        radius = 300  
        center_x, center_y = 600, 400  

        # positions of the nodes
        positions = [
            (
                center_x + radius * math.cos(2 * math.pi * i / num_nodes),
                center_y + radius * math.sin(2 * math.pi * i / num_nodes),
            )
            for i in range(num_nodes)
        ]

        # draw the edges
        for i in range(num_nodes):
            for j in range(i + 1, num_nodes):  
                # check if there is an edge between the nodes
                if matrix[i][j] != 0: 
                    x1, y1 = positions[i]
                    x2, y2 = positions[j]
                    self.canvas.create_line(x1, y1, x2, y2, fill="black")
                    weight_x = (x1 + x2) / 2
                    weight_y = (y1 + y2) / 2
                    self.canvas.create_text(weight_x, weight_y, text=str(matrix[i][j]), fill="red")

        # draw the nodes
        for i, (x, y) in enumerate(positions):
            self.canvas.create_oval(x - 20, y - 20, x + 20, y + 20, fill="lightblue", outline="black")
            self.canvas.create_text(x, y, text=str(i), fill="black")

    def update_tables(self):
        # clear the tables frame
        for widget in self.tables_frame.winfo_children():
            widget.destroy()

        tables = self.network.get_tables()
        row_offset = 0
        # loop through each router
        for node, connections in tables.items():
            # create a label for the router
            tk.Label(self.tables_frame, text=f"Node {node}", font=("Arial", 12, "bold")).grid(row=row_offset, column=0, pady=10, padx=5, sticky="w")
            # create labels for the table
            tk.Label(self.tables_frame, text="Destination", width=12, anchor="w").grid(row=row_offset + 1, column=1, padx=5)
            # create labels for the table
            tk.Label(self.tables_frame, text="Cost", width=12, anchor="w").grid(row=row_offset + 1, column=2, padx=5)
            # create labels for the table
            tk.Label(self.tables_frame, text="Next Hop", width=12, anchor="w").grid(row=row_offset + 1, column=3, padx=5)

            # loop through each connection
            for i, (destination, info) in enumerate(connections.items()):
                tk.Label(self.tables_frame, text=str(destination), width=12, anchor="w").grid(row=row_offset + 2 + i, column=1, padx=5)
                tk.Label(self.tables_frame, text=str(info[0]), width=12, anchor="w").grid(row=row_offset + 2 + i, column=2, padx=5)
                tk.Label(self.tables_frame, text=str(info[1]), width=12, anchor="w").grid(row=row_offset + 2 + i, column=3, padx=5)
            # update the row offset
            row_offset += len(connections) + 3
