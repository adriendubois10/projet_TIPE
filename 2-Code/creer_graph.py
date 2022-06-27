import networkx as nx
import matplotlib.pyplot as plt

G1 = nx.Graph()
S1 = [(1,4),(1,6),(1,2),(2,5),(2,3),(3,6),(3,4),(4,5),(5,6)]
for (i,j) in S1:
    G1.add_edge(i, j)

G2 = nx.Graph()
S2 = [(1,2),(1,4),(1,6),(2,3),(2,5),(3,4),(3,6),(4,5),(5,6)]
for (i,j) in S2:
    G2.add_edge(i, j)
    
sigma = [0, 3, 6, 5, 4, 1, 2] #0 pour l'indexation
S_permut = [(sigma[i],sigma[j]) for (i,j) in S1]
G_permut = nx.Graph()
for (i,j) in S_permut:
    G_permut.add_edge(i, j)

# explicitly set positions
pos1 = {1: (0, 0), 2: (1,0), 3: (2,1), 4: (1,2), 5: (0,2), 6: (-1,1)}
pos2 = {1: (0,2), 2: (0.9,1.4), 3: (1.5,0.5), 4: (2,2), 5: (2.5,1), 6: (1,-1)}
pos_permut = {sigma[k]: pos1[k] for k in pos1.keys()}

options = {
    "font_size": 36,
    "node_size": 2000,
    "node_color": "white",
    "edgecolors": "black",
    "linewidths": 5,
    "width": 5,
}

#nx.draw_networkx(G1, pos1, **options)
nx.draw_networkx(G_permut, pos_permut, **options)
#nx.draw_networkx(G2, pos2, **options)

# Set margins for the axes so that nodes aren't clipped
ax = plt.gca()
ax.margins(0.20)
plt.axis("off")
plt.show()