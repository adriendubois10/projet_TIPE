from def_protein import *

#generer proteine    
#generation 2 : 4 liaisons par carbone, 1 par hygrogène, 3 par azote, etc -> pbm de satisfiabilité (incroyable)

def liste_cercle(liste_atom):
    return [[x.point, 0, x.point.copy(), x.indice] for x in liste_atom] #on conserve l'indice initial
            
def contact(i,j,lc):
        return distance(lc[i][0] ,lc[j][0]) <= (lc[i][1] + lc[j][1])
        
def update(lc, n, fixe, trans): #n=len(lc)
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
                
def incrementer(lc, n, fixe, trans, eps, rmax):
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
    lcouples = [ (tuple(lc[i][2]),tuple(lc[j][2])) for i in range(n) for j in fixe[i] ]
    n, k = len(lcouples), 0
    while k < n:
        if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
            lcouples.pop(k)
            n += -1
        else:
            k += 1
    return lcouples

def tri_denombrement(l,N): #N nbr sommets
    compt = [False]*N
    for x in l:
        compt[x] = True
    return [x for x in range(N) if compt[x]]
    

#si le graphe n'est pas connexe, relier les composantes connexes

def connexe(g): #retounre partition des sommets
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

def dmin(l1, l): 
    dm, xm, ym = distance(lc[l1[0]][2],lc[l[0][0]][2]), l1[0], l[0][0]
    for l2 in l:
        for x in l1:
            for y in l2:
                d = distance(lc[x][2],lc[y][2])
                if d<dm:
                    dm, xm, ym = d, x, y
    return xm, ym, dm

def dmax(l,lc):
    n = len(l)
    dm, xm, ym = distance(lc[l[0]][2],lc[l[1]][2]), l[0], l[1]
    for i in range(n-1):
        for j in range(i+1,n):
            x, y = l[i], l[j]
            d = distance(lc[x][2],lc[y][2])
            if d>dm:
                dm, xm, ym = d, x, y
    return xm, ym, dm

def relier(g, lc): #sortie -> un graphe connexe
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

# def indice_max(l):
#     n = len(l)
#     if n==0:
#         return -1
#     mini, i0 = l[0], 0
#     for i in range(n):
#         if l[i] > mini:
#             mini, i0 = l[i], i
#     return i0

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
    print('démarrage')
    C = cycles(g,n)
    print('fin')
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

#génération

def gen_carbones(prot):
    '''Entrée : protéine sans liaisons
       Sortie : protéine avec liaisons carbones'''
    
    carbones = Protein(prot.extraire_molecule('C'), [])
    lc = liste_cercle(carbones)
    n = len(lc) #nbr de carbones
    eps = ecart_type([distance(lc[i][0],lc[j][0]) for i in range(n) for j in range(i+1,n)])/100
    fixe = [False]*n # future liste d'adjacence du graphe carbone
    trans = [False]*n
    rmax = dmax([i for i in range(prot.nbr)],lc)
        
    while False in fixe:
        incrementer(lc, n, fixe, trans, eps, rmax) 
        update(lc, n, fixe, trans)
        
    #ici, les carbones sont reliés, mais composantes non connexes et/ou cycles qui correspondent à des arêtes inutiles
        
    relier(fixe, lc)
    enlever_cycles(fixe, lc, n)
    
    #on a alors obtenu un "arbre couvrant" reliant les carbones, reste à convertir en format Protein
    #on reporte les connections à la protéine entière
    connections = [[] for _ in range(prot.nbr)]
    for i in range(n):
        for j in fixe[i]:
            connections[ lc[i][3] ].append( lc[j][3] )
        
    return Protein(prot.latom, connections)

#ALTERNATIVE (plus simple) : on traite de la même manière toutes les molécules

def gen_uniforme(prot):
    lc = liste_cercle(prot.latom)
    eps = ecart_type([distance(lc[i][0],lc[j][0]) for i in range(prot.nbr-1) for j in range(i+1,prot.nbr)])/100
    fixe = [False]*prot.nbr # future liste d'adjacence du graphe
    trans = [False]*prot.nbr
    rmax = dmax([i for i in range(prot.nbr)],lc)[2]
        
    while False in fixe:
        incrementer(lc, prot.nbr, fixe, trans, eps, rmax) 
        update(lc, prot.nbr, fixe, trans)
    print('ok')    
    relier(fixe, lc)
    print('ok1')
    enlever_cycles(fixe, lc, prot.nbr)
    print('ok2')

    return Protein(prot.latom, fixe)    

#supprimer les molécules seules

import sys
sys.path.insert(0, "anim2D")
from gencarbones2D import connexe

def filtre(prot,li):
    latom = [Atom(li.index(k), prot.latom[k].point, prot.latom[k].atom) for k in li]
    connect = [[li.index(v) for v in inter2(li,prot.connect[s])] for s in li]        
    return Protein(latom, connect)

def filtre_liaisons(prot):
    comp = connexe(prot.connect)
    comp_max = comp[indice_max([len(c) for c in comp])]
    li = [] #liste des sommets gardés
    for s in comp_max:
        if not s in li:
            li.append(s)
    return filtre(prot,li)

def filtre_RE(prot):
    li = [k for k in range(prot.nbr) if prot.latom[k].atom in ['C','N','O','H','S']]
    return filtre(prot,li)

def filtre_nbr(prot,nbr_lim):
    li = [i for i in range(min(nbr_lim,prot.nbr))]
    return filtre(prot,li)
    

#plier la proteines -> diapo 2 structures isom positions diff

def indice_point_mileu(prot):
    paires = [(i,j) for i in range(prot.nbr) for j in range(prot.nbr)]
    l_diam = [distance(prot.liste[i], prot.liste[j]) for (i,j) in paires]
    i,j = paires[indice_max(l_diam)] #indices des points les plus éloignés
    pos_milieu = [ (prot.liste[i][k]+prot.liste[j][k])/2 for k in [0,1,2] ]
    return (prot.latom[ indice_min([distance(prot.liste[i],pos_milieu) for i in range(prot.nbr)]) ]).indice
    
def plier(prot):
    im = indice_point_mileu(prot)
    select = [i for i in range(prot.nbr) if prot.liste[i][2]<=prot.liste[im][2]] #points au dessus de i
    #lrot = rotation_z([prot.liste[i] for i in select],prot.liste[im][0],prot.liste[im][1]) pas de changements ?
    lpos, k = [], 0
    for i in range(prot.nbr):
        if i in select:
            lpos.append([prot.liste[i][0],prot.liste[i][1]+(prot.liste[i][2]-prot.liste[im][2]), prot.liste[i][2]])
            k+=1
        else:
            lpos.append(prot.liste[i])
    return Protein( [Atom((prot.latom[i]).indice, lpos[i], (prot.latom[i]).atom) for i in range(prot.nbr)], prot.connect )

#liason proche aléatoire (minimiser la taille des paquets)

def liaison_proche(prot,adj,i):
    im = indice_min([distance(prot.latom[i].point, prot.latom[j].point) for j in range(prot.nbr) if (j!=i and not j in adj[i])])
    adj[i].append(im)
    adj[im].append(i)
    
def ajouter_liaisons(prot,adj,p=0.1): #p proportion
    p = int(np.ceil(p * prot.nbr))
    for _ in range(p):
        i = rd.randint(0,prot.nbr-1)
        liaison_proche(prot,adj,i)
        
#méthode 2 : arbre couvrant

from arbre_couvrant import *

def gen_couvrant(prot, ajout=0): #ajout entre 0 et 1 proportion de liaisons en plus
    mat_dist = prot.matrice_dist()
    g = [[(j,mat_dist[i][j]) for j in range(prot.nbr)] for i in range(prot.nbr)]
    liste_couvrante = ACM(g)
    adj = [[] for _ in range(prot.nbr)]
    for (i,j) in liste_couvrante:
        adj[i].append(j)
        adj[j].append(i)

    if ajout!=0:
        ajouter_liaisons(prot,adj,ajout)

    return Protein(prot.latom, adj)
    
        
#générer une permuation de la protéine -> inverser k to n-1-k

def permut_prot(prot):
    def inv(k):
        return prot.nbr-1-k
    latom_inv = [Atom(inv(prot.latom[inv(i)].indice), prot.latom[inv(i)].point, prot.latom[inv(i)].atom) for i in range(prot.nbr)]
    connect_inv = [[inv(s) for s in prot.connect[inv(i)]] for i in range(prot.nbr)]
    return Protein(latom_inv, connect_inv)

#légèrement bouger les positions

def shuffle_trans(prot):
    for i in range(prot.nbr):
        prot.latom[i].point[1] += 1 * rd.random()
    
    

      
    
        
    
    
        
