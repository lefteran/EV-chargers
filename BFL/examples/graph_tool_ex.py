
import graph_tool.all as gt

g = gt.Graph(directed=False)

v1 = g.add_vertex()
v2 = g.add_vertex()
e = g.add_edge(v1, v2)
print(v1.out_degree())
print(e.source(), e.target())
vlist = g.add_vertex(10)
print(len(list(vlist)))

v = g.add_vertex()
print(g.vertex_index[v2])

g.remove_vertex(v2)
print(e.source(), e.target())
g.remove_edge(e)