import numpy as np
import random as rd
from matplotlib.pyplot import pause
import print_graph as pg

#divers

def distance(a,b):
    return np.sqrt( (a[0]-b[0])**2 + (a[1]-b[1])**2 )

def rand(a,b):
    return a + rd.random()*(b-a)

def gen_points(n, xlim, ylim):
    return [[ int(rand(*xlim)), int(rand(*ylim)) ] for _ in range(n)]

def esperance(l):
    return sum(l)/len(l)

def variance(l):
    e1 = esperance([x**2 for x in l])
    e2 = esperance(l)**2
    return e1 - e2

def ecart_type(l):
    return np.sqrt(variance(l))
    
#cercles
        
def liste_cercle(liste): #liste des [centre à translater, rayon, centre de référence]
    return [[x, 0, x.copy()] for x in liste]
        
def contact(i,j,lc):
        return distance(lc[i][0] ,lc[j][0]) <= (lc[i][1] + lc[j][1])
    
def update(lc, n, fixe, trans, continuer=True): #n=len(lc)
    if not continuer:
        return 
    for i in range(n):
        count, ref = 0, []
        for j in [k for k in range(n) if k!=i]:
            if contact(i,j,lc):
                count += 1
                ref.append(j)
        if count>=2:
            fixe[i] = ref
        if count==1:
            trans[i] = ref[0]
            
def incrementer(lc, n, fixe, trans, eps, rmax, continuer=True):
    if not continuer:
        return None
    for i in range(n):
        if fixe[i]!=False:
            pass
        elif trans[i]!=False:
            a = lc[trans[i]][0]
            b = lc[i][0]
            AB = np.array(b)-np.array(a)
            lc[i][0] = ( np.array(b) + eps * (AB)/distance(a,b) ).tolist()
            lc[i][1] += eps
        else:
            lc[i][1] += eps
    r = max([lc[i][1] for i in range(n)])
    if r > rmax:
        for i in range(n):
            if fixe[i]==False:
                fixe[i] = [trans[i]]

def vertices(lc, fixe, n): 
    def maxi(liste):
        if liste==[]:
            return 0
        return max(liste)
    def rev(couple):
        a,b=couple
        return b,a
    lcouples = [ (lc[i][2],lc[j][2]) for i in range(n) for j in fixe[i] ]
    n, k = len(lcouples), 0
    while k < n:
        if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
            lcouples.pop(k)
            n += -1
        else:
            k += 1
    return lcouples

#si le graphe n'est pas connexe, relier les composantes connexes

g_ex = [ [3], [4,2], [1,4], [0], [1,2] ]
g1 = [ [1], [0,2,3], [1,3], [1,2] ]
d1 = [[0,1,0,0],
      [1,0,1,0],
      [0,1,0,2],
      [0,1,2,0]]

def connexe1(g): #entrée : liste d'adjacence, sortie : partition des sommets
    n = len(g)
    s = [i for i in range(n)]
    for k in range(n):
        for l in range(len(g[k])):
            if s[k]<s[ g[k][l] ]:
                s[ g[k][l] ] = s[k]
            else:
                s[k] = s[ g[k][l] ]
                #print('sommet :', k, ' ; voisin :', g[k][l], ' ; s :', s)
    m = max(s)
    return [x for x in [ [k for k in range(n) if s[k]==j] for j in range(m+1) ] if x!=[]]

def connexe2(g):
    c = []
    for i in range(len(g)):
        ic = -1
        for j in range(len(c)):
            for u in g[i]:
                if u in c[j]:
                    if ic==-1:
                        ic = j   
        if ic!=-1:
            c[ic].append(i)
        else:
            c.append([i])
    return c

def connexe(g,prot=False):
    if prot:
        g = g.connect
    n = len(g)
    T = [False for _ in range(n)]
    a_visiter = [0]
    T[0] = True
    comp_connexes = []
    for i in range(n):
        if not T[i]:
            a_visiter = [i]
            T[i] = True
            comp = []
            while a_visiter != []:
                s = a_visiter.pop(0)
                comp.append(s)
                for x in g[s]:
                 if not T[x]:
                    T[x] = True
                    a_visiter.append(x)
            comp_connexes.append(comp)
    return comp_connexes
        
            

def est_connexe(g):
    return len(connexe(g))==1

def est_connexe_sans(g, arete):
    a, b = arete
    h = [[y for y in x] for x in g]
    if b in g[a]:
        h[a].remove(b)
    if a in g[b]:
        h[b].remove(a)
    return est_connexe(h)
        
def relier_ssdist(g):
    c = connexe(g)
    n = len(c)-1
    while n>1:
        g[ c[0][-1] ].append( c[1][0] )
        g[ c[1][0] ].append( c[0][-1] )
        c = connexe(g)
        n += -1
        
#def relier(g,lc):
#    return relier_ssdist(g)

def relier(g, lc):
    def dmin(l1, l): 
        dm, xm, ym = distance(lc[l1[0]][2],lc[l[0][0]][2]), l1[0], l[0][0]
        for l2 in l:
            for x in l1:
                for y in l2:
                    d = distance(lc[x][2],lc[y][2])
                    if d<dm:
                        dm, xm, ym = d, x, y
        return xm, ym, dm
    c = connexe(g)
    n = len(c)
    while n>1:
        x, y, d = dmin(c[0],c[1:])
        g[ x].append( y )
        g[ y ].append( x )
        c = connexe(g)
        n += -1
    
                
     
#retirer cycles

#A) Trouver cycles -> liste des cycles représentés par une liste des indices des arêtes
               
def tri_denombrement(l,N): #N nbr sommets
    compt = [False]*N
    for x in l:
        compt[x] = True
    return [x for x in range(N) if compt[x]]

def cycle_min(s0,g,n):
    chemins = [ [s0] ]
    new_chemins = []
    while chemins!=[]:
        new_chemins = []
        for chemin in chemins:
            for s in g[ chemin[-1] ]:
                if not s in chemin:
                    if s0 in g[s] and len(chemin)>1:
                        chemin.append(s)
                        return tri_denombrement(chemin,n)
                    new_chemins.append(chemin+[s])
        chemins = new_chemins
    return []
                                
def sans_repet(l):
    n = len(l)
    if n<=1:
        return l
    if l[0] in l[1:] or l[0]==[]:
        return sans_repet(l[1:])
    return [l[0]]+sans_repet(l[1:])

def cycles(g,n):
    lcyclesmin = []
    for s in range(n):
        c = cycle_min(s,g,n)
        if c!=[]:
            lcyclesmin.append( c )
    return sans_repet(lcyclesmin)
    
#B) Pour chaque cycle, enlever l'arete de distance maximale -> retourne un graphe connexe dit arbre (connexe sans cycle)

def indice_max(l):
    n = len(l)
    if n==0:
        return -1
    mini, i0 = l[0], 0
    for i in range(n):
        if l[i] > mini:
            mini, i0 = l[i], i
    return i0

def indmaxparmi(l, lt, n):
    m = max([l[i] for i in range(n) if not lt[i]])
    for i in range(n):
        if l[i]==m and not lt[i]:
            return i

def tri_ind(l):
    n = len(l)
    lt = [False for _ in range(n)]
    lp = []
    while False in lt:
        im = indmaxparmi(l, lt, n)
        lt[im] = True
        lp.append(im)
    return lp
        

def enlever_poids_max(cycle, aretes_enlevees, lpoints, g):
    c = len(cycle)
    l_aretes = [(cycle[i],cycle[j]) for i in range(c-1) for j in range(i+1,c) if (cycle[j] in g[cycle[i]]) and not ((cycle[i],cycle[j]) in aretes_enlevees) and not ((cycle[j],cycle[i]) in aretes_enlevees)]
    ldist = [distance(lpoints[i][2],lpoints[j][2]) for (i,j) in l_aretes]
    im = indice_max(ldist)
    if im!=-1:
        ti = tri_ind(ldist)
        n = len(l_aretes)
        i = 0
        while i<n and not est_connexe_sans(g, l_aretes[ti[i]]):
            i+=1
        if not est_connexe_sans(g, l_aretes[ti[n-1]]):
            return None
        a, b = l_aretes[ti[i]]
        aretes_enlevees.append((a,b))
        aretes_enlevees.append((b,a))

def enlever_cycles(g, lpoints, n):
    C = cycles(g,n)
    print(' ')
    aretes_enlevees = []
    for cycle in C:
        enlever_poids_max(cycle, aretes_enlevees, lpoints, g)
    for (a,b) in aretes_enlevees:
        if b in g[a]:
            g[a].remove(b)
        if a in g[b]:
            g[b].remove(a)
    return aretes_enlevees

#OU Kruskal



