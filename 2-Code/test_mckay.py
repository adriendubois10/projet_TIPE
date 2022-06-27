from graphisomorphism import *
import networkx as nx
import matplotlib.pyplot as plt

G1 = Graph([0,1,2,3,4,5,6,7,8], [[1,3], [0,2,4], [1,5], [0,4,6],[1,5,7,3],[2,4,8],[3,7],[4,6,8],[5,7]]) #exemple page 6

#affichage

def show(G=G1,sigma='id',center=False):
    pos = {1:(0,2),2:(1,2.3), 3:(2,2), 4:(-0.3,1), 5:(1.3,1), 6:(2.3,1), 7:(0,0), 8:(1,-0.3), 9:(2,0)}
    if center:
        pos = {1:(0,2),2:(1,2), 3:(2,2), 4:(0,1), 5:(1,1), 6:(2,1), 7:(0,0), 8:(1,0), 9:(2,0)}
    if sigma=='id':
        pos_sigma= pos
    else:
        pos_sigma = {(sigma[k-1]+1):pos[k] for k in pos.keys()}
    G_print = nx.Graph()
    for i in range(G.nbr):
        for j in G.connect[i]:
            if sigma=='id':
                G_print.add_edge(i+1,j+1)
            else:
                G_print.add_edge(sigma[i]+1,sigma[j]+1)
    options = { 
        "font_size": 36,
        "node_size": 2000,
        "node_color": "white",
        "edgecolors": "black",
        "linewidths": 5,
        "width": 5} #["white","white","white",[0.36, 0.54, 0.66],"white","red",[0.36, 0.54, 0.66],"red",[0.36, 0.54, 0.66]],
    nx.draw_networkx(G_print, pos_sigma, **options)
    ax = plt.gca()
    ax.margins(0.20)
    plt.axis("off")
    ax.set_aspect('equal')
    plt.show()
    
#test fonctions
    
# print( deg(G1,6,[1]) )
# print( shatters(G1,[3,7],[6,8]))

# pi1 = [[0,1,2,3,4,5,6,7,8]]
# pi2 = [ [0],[2,6,8],[1,3,5,7],[4] ]
# refinement(G1,pi2)

# pi3 = [[0,2,6,8],[1,3,5,7],[4]]
# #permut = permutations_tree(G1, pi3)
# 

pideg = [[0,2,6,8], [1,3,5,7], [4]]
sG = search_tree(G1, pideg)

CmG,sigma = Cm(G1,pideg)
show(G1,sigma,True)

print(sigma)








    





