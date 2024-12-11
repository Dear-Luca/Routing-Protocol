from network import Network

graph1 = [[0, 2, 0, 4, 0, 0],
          [2, 0, 1, 0, 0, 0],
          [0, 1, 0, 3, 5, 0],
          [4, 0, 3, 0, 0, 2],
          [0, 0, 5, 0, 0, 6],
          [0, 0, 0, 2, 6, 0]]
network1 = Network("Network1", graph1)
print(network1)
network1.print_tables()