import networkx as nx

nodes = [1,2,3,4,5,6,7,8,9]

graph = nx.Graph()
for node in nodes:
    graph.add_node(node)

graph.add_edge(1, 2)
graph.add_edge(1, 9)

independent_set = nx.maximal_independent_set(graph)
print(independent_set)