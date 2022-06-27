import matplotlib.pyplot as plt
import networkx as nx
from numpy import array

def graph2nx(H, red=[]): #liste d'adjacence vers format nx
    n = len(H)
    G = nx.Graph()
    def rev(couple):
        a,b=couple
        return b,a
    lcouples = [(a,b) for a in range(n) for b in H[a]]
    n, k = len(lcouples), 0
    while k < n:
        if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
            lcouples.pop(k)
            n += -1
        else:
            k += 1
    for s in range(len(H)):
        G.add_node(s)
    for (a,b) in lcouples:   
        if (a,b) in red:
            G.add_edge(a,b, color='red')
        else:
            G.add_edge(a,b)
    return G
    
def show(H):
    G = graph2nx(H)
    # positions for all nodes
    pos = nx.spring_layout(G)
    # nodes
    nx.draw_networkx_nodes(G, pos, node_size=800,alpha=0.9)             
    # labels
    nx.draw_networkx_labels(G, pos,font_size=20)
    # edges
    nx.draw_networkx_edges(G, pos,width=1)
    nx.draw_networkx_edge_labels(G, pos)
    plt.axis('off')
    plt.show()
