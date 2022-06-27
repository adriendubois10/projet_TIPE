from heapq import *
import numpy as np
import matplotlib.pyplot as plt

# G = [[(4 , 60) , (5, 100)], [(2, 20) , (3, 30) , (4 ,40)],
# [(1 , 20) , (3, 10)], [(1, 30) , (2, 10) , (4, 50)],
# [(0 , 60) , (1, 40) , (3, 50) , (5, 70)], [(0, 100) , (4, 70) ]]

def taille(g):
    return len(g)

def voisins(g, s):
    return g[s]

def aretes_poids(g, s, vu):
    return [(p,s,i) for (i,p) in g[s] if (vu[i]+vu[s])==1]

def ss_doublons(lcouples):
    def rev(couple):
        p,a,b=couple
        return p,b,a
    n, k = len(lcouples), 0
    while k < n:
        if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
            lcouples.pop(k)
            n += -1
        else:
            k += 1
    return lcouples


def ajout(file, trip):
    heappush(file, trip)
    
def ACM(g):
    n = len(g)
    vu = [True]+[False]*(n-1)
    poids_min = []
    while len(poids_min)<(n-1):
        aretes = []
        for i in range(n):
            if not vu[i]:
                ap = aretes_poids(g,i,vu)
                for trip in ap:
                    ajout(aretes, trip)
        p,i,j = heappop(aretes)
        vu[i], vu[j] = True, True
        poids_min.append( (i,j) )
    return poids_min