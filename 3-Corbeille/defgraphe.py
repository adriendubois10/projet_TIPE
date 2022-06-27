import random as rd
from math import *
import matplotlib.pyplot as plt

#prérequis : fonctions utiles

def ensemblecouples(l):
    '''Entrée : liste
       Sortie : ensemble des couples distincts sans ordre de la liste'''
    n, couples = len(l), []
    for i in range(n-1):
        for j in range(i+1,n):
            couples.append( (l[i],l[j]) )
    return couples

def distance(a,b):
    ''' Entrée : 2 points représentés par le couple abcisse/ordonnée
        Sortie : distance entre ces points'''
    return sqrt( ( a[0]-b[0] )**2 + ( a[1]-b[1] )**2 )

def listelettres(n):
    '''Entrée : entier naturel n non nul
       Sortie : liste de n lettres à associer à des points, ex: [A,B,...,Z,A1,...]'''
    L = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    return L[:n] + ["{}{}".format(L[i%26], i//26) for i in range(26,n)]


#Graphes
#On définit un type de graphe particulier : d'ordinaire noté G(X,U) avec X l'ensemble de sommets et U l'ensemble des relations,
#on considère G'(X) = G(X,U) avec U l'ensemble des relation entre tous les sommets du graphe non-orienté
#on notera G' = Graphepoints

class Graphepoints:
    
    def __init__(self, l):
        self.N = len(l)
        self.edges = ensemblecouples( l ) #graphe non orienté, n(n-1)/2 relations si len(l)=n
        self.nodes = l #ensemble des points
        self.point = listelettres(self.N) #nom des points de A,..,Z,A1,..
        self.mat = [[ distance(self.nodes[i],self.nodes[j]) for j in range(i+1,self.N)] for i in range(self.N)]  # matrice de terme courant mij = dist(l[i],l[j]), les zéros ne sont pas comptés, ni les distance inverses   
    
    
    def show(self, xlimite=100, ylimite=100):
        
        fig, ax = plt.subplots( figsize = (xlimite,ylimite) ) #scale the axis
        
        def lignedistance(A, B, dist): #relie 2 points et marque leur distance
            plt.plot( [A[0], B[0]], [A[1], B[1]], color = 'black') #trace la ligne entre 2 points
            bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
            ax.text( (A[0]+B[0])/2, (A[1]+B[1])/2, str(dist) , ha="center", va="center", size=10,bbox=bbox_props) #affiche la distance au centreù
            
        for i in range(self.N):
            x,y = self.nodes[i][0], self.nodes[i][1]
            plt.scatter(x, y, linewidth = 0.05*ylimite)
            plt.annotate(self.point[i], (x,y), xytext = (x+1,y+1), size = 0.15*ylimite)
            for j in range(i+1,self.N):
                lignedistance(self.nodes[i], self.nodes[j], round( self.mat[i][j-i-1], 1) )
                
        plt.xlim(0, xlimite)
        plt.ylim(0,ylimite)
        ax.xaxis.set_ticks_position('both') #axes en haut et en bas
        ax.yaxis.set_ticks_position('both') #axes sur les côtés
        ax.set_aspect('equal') #repère orthonormé si xlim=ylim -> à ameliorer si xlim != ylim
        plt.show()
    
#On se place dans un carré de 100u de côté
a = rd.randint(0,100),rd.randint(0,100)
b = rd.randint(0,100),rd.randint(0,100)
c = rd.randint(0,100),rd.randint(0,100)
G = Graphepoints( [a, b, c] )
print(' G (X, U) ' )
print( 'Les noeuds ( ensemble X ) de G sont : {}'.format(G.nodes) )
print( 'Les arêtes ou arcs ( ensemble U ) de G sont : {}'.format(G.edges) )
print( 'La matrice d\'adjacence de G est : {}'.format(G.mat) )
print( 'Le nombre de sommets est |X| = {} '.format(G.N) )

def nuagepoint(n,a,b):
    return Graphepoints( [(rd.randint(0,a),rd.randint(0,b)) for i in range(n)] )

G1 = nuagepoint(5,100,100)

#Affichage

def affichergraphe(G,xlimite=100,ylimite=100):
    fig, ax = plt.subplots( figsize = (xlimite,ylimite) )
    
    def lignedistance(A, B, dist):
        plt.plot( [A[0], B[0]], [A[1], B[1]], color = 'black')
        bbox_props = dict(boxstyle="round", fc="w", ec="0.5", alpha=0.9)
        ax.text( (A[0]+B[0])/2, (A[1]+B[1])/2, str(dist) , ha="center", va="center", size=20,bbox=bbox_props)
        plt.show()
        
    for i in range(len(G.nodes)):
        x,y = G.nodes[i][0], G.nodes[i][1]
        plt.scatter(x, y, linewidth = 5)
        plt.annotate(G.point[i], (x,y), xytext = (x+1,y+1), size = 15)
        
    plt.xlim(0, xlimite)
    plt.ylim(0,ylimite)
    ax.xaxis.set_ticks_position('both') #axes en haut et en bas
    ax.yaxis.set_ticks_position('both') #axes sur les côtés
    ax.set_aspect('equal') #repère orthonormé
    plt.show()
    
    
