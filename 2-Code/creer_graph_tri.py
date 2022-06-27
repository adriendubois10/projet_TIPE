import networkx as nx
import matplotlib.pyplot as plt

Gr = nx.Graph()
Sr = [(1,4),(2,4),(4,5),(3,5)]
for (i,j) in Sr:
    Gr.add_edge(i, j)


# explicitly set positions
pos = {1: (0, 0), 2: (1,0), 3: (2,0), 4: (0.5,1), 5: (1.5,1)}

options = {
    "font_color": "black",
    "font_size": 36,
    "node_size": 2000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5}

nx.draw_networkx(Gr, pos, **options)

ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()