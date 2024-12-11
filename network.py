class Network:
    def __init__(self, adj_matrix: list[list[int]] = None) -> None:
        """Constructor for the Network class.

        Args:
            adj_matrix (list[list[int]], optional): The adjacency matrix of the network. Defaults to None.
        """
        self.tables = {}
        self.routers = self.graph_build(adj_matrix)

    def graph_build(self, adj_matrix: list[list[int]]) -> dict[int, dict[int, int]]:
        """Builds the network graph.

        Args:
            adj_matrix (list[list[int]]): The adjacency matrix of the network.

        Returns:
            dict[int, dict[int, int]]: The network graph.
        """
        routers = {}
        for row in range(len(adj_matrix)):
            routers[row] = {}
            self.tables[row] = {}
            self.tables[row][row] = (0, None) 
            for col in range(len(adj_matrix[row])):
                if adj_matrix[row][col] != 0:
                    routers[row][col] = adj_matrix[row][col]
                    self.tables[row][col] = (adj_matrix[row][col], col)
        return routers
    
    def update_tables(self)-> None:
        """Updates the tables of the network.
        """
        # loop through each router
        for router in self.routers:
            # visit the neighbors of the current router
            for neigh in self.routers[router]:
                # use the distance vector of the neighbors to update the table of the current router
                for node, distance_vector in self.tables[neigh].items():
                    # if the node is not the current router and the node is not in the table of the current router
                    if node != router and node not in self.tables[router]:
                        # update the table of the current router
                        self.tables[router][node] = (self.tables[router][neigh][0] + distance_vector[0], neigh)
                    # if the node is not the current router and the node is in the table of the current router
                    elif node != router:
                        # if the distance vector of the current node is less than the distance vector of the node in the table of the current router
                        if self.tables[router][neigh][0] + distance_vector[0] < self.tables[router][node][0]:
                            # update the table of the current router
                            self.tables[router][node] = (self.tables[router][neigh][0] + distance_vector[0], neigh)
                
    def get_tables(self) -> dict[int, dict[int, int]]:
        """Returns the tables of the network.

        Returns:
            dict[int, dict[int, int]]: The tables of the network.
        """
        return self.tables
    
    def print_tables(self) -> None:
        """Prints the tables of the network.
        """
        for router, connections in self.tables.items():
            print(f"Router {router}: {connections}")

    def __str__(self) -> str:
        """String representation of the Network class.

        Returns:
            str: The string representation of the Network
        """
        routers_str = "\n".join(f"{router}: {connections}" for router, connections in self.routers.items())
        return f"Network: {self.name}\nRouters:\n{routers_str}"