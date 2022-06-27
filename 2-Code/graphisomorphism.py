from geometrie_et_aux import *

class Graph:
    
    def __init__(self, vertices, connect): #connexions liste de taille len(lmol) où connexions[i] est une liste des indices des molecules connectées
        self. vertices = vertices #majoritairement [|0,n-1|]
        self.nbr = len(vertices)
        self.connect = [sans_repet(l) for l in connect] #liste d'adj
        
    def edges(self): #liste des aretes : non-orienté
        def maxi(liste):
            if liste==[]:
                return 0
            return max(liste)
        def rev(couple):
            a,b=couple
            return b,a
        lcouples = [ (self.vertices[i],self.vertices[j]) for i in range(self.nbr) for j in self.connect[i] ]
        n, k = len(lcouples), 0
        while k < n:
            if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
                lcouples.pop(k)
                n += -1
            else:
                k += 1
        return lcouples
    
    def ldegre(self):
        return [len(self.connect[i]) for i in range(self.nbr)]
    
    def sort_by_degre(self): #liste tq l[i] ensemble des sommets de degre i
        ldeg = self.ldegre()
        ld = [ [s for s in range(self.nbr) if ldeg[s]==i] for i in range(max(ldeg)+1) ]
        return [l for l in ld if l!=[]]
    
G = Graph([0,1,2],[[1],[2],[0]])
H = Graph([0,1,2],[[2,1],[0],[1]])

#naif -> fact(|S|)

def test_isomorphism(G, H, f):
    for i in range(G.nbr):
        if not [f[j] for j in G.connect[ f[i] ]] == H.connect[i]:
            break
        if i==(G.nbr-1):
            return True, f
    return False, []

def test_isomorphism2(G,H,f,g):
    for i in range(G.nbr):
        if not [f[j] for j in G.connect[ f[i] ]] == [g[j] for j in H.connect[ g[i] ]]:
            break
        if i==(G.nbr-1):
            return True, composee(inverse(g),f)
    return False, []

def isomorphism(G,H):
    if G.nbr != H.nbr:
        return False, []
    Imf = permutations(G.nbr)
    for f in Imf:
        res = test_isomorphism(G, H, f)
        if res != (False, []):
            return res
    return False, []


#v2 -> choix d'invariants (degré, type du sommet,  pour permutations en paquet)

#tris des sommets
    
def inter2(l1,l2):
    return [i for i in l1 if i in l2]
    
def intersection(l, n): #l une liste de liste d'indices, n = len(l)
    i0 = indice_min([len(x) for x in l])
    inter, i = l[i0], 0
    while inter != [] and i<n:
        inter = inter2(inter,l[i])
        i += 1
    return inter

def cas_vide(Li,numi):
    if Li==[]:
        return []
    return Li[numi]
      
def assoc_canonique(L): #L est une liste de partition de [0,n-1], attention ordre important / on combine len(L) tris de sommets pour créer un tri encore plus efficace de manière unique
    tri = [] #nouveau tri qui combine tous les autres
    l_len, tl = [max(0,len(l)-1) for l in L], len(L)
    num, i =  [-1]+[0]*(tl-1), 0
    while i<tl:
        if num[i]<l_len[i]:
            num[i] += 1
            liste_inter = [ cas_vide(L[i],num[i]) for i in range(tl)]
            x = intersection(liste_inter, tl)
            if x != []:
                tri.append(x)
            i = 0
        while i<tl and num[i]==l_len[i]:
            num[i] = 0
            i += 1 
    return tri

#A] on fixe la taille max d'un paquet et on calcule p : toutes les permutations de [1,n] pour n allant de 0 à taille max (0 <- [], 1 <- [[0]], ...)
#B] pour un paquet de taille k, k! permutaions possibles -> elles sont numérotées dans p[k] liste de ces k! permuatation
#   Ainsi, si un numéro est une suite d'indice (représentée par une liste) des permutaions d'un paquet, on itère sur tous les numéros
#C] Pour chaque numéro, on crée alors une bijection des sommets de G vers H, qui conserve les invariants des sommets
    

def concatenation(num, triG, triH, nb_paquets, tailles_paquets, p ): #permut dynamique p variable globale(non), num une numérotation, lentri la longueur(commune) des listes, l_lentri liste des tailles des paquets
    maxi_nbr = max([max(e) for e in triG])+1
    concat = [0]*maxi_nbr
    for i in range(nb_paquets): #parcours des paquets de tri
        for j in range(tailles_paquets[i]): #parcours des élément d'un même paquet et association avec la permutation choisie par num
            j_permut = p[tailles_paquets[i]][num[i]][j] 
            concat[ triG[i][j] ] = triH[i][j_permut] # sommet j associé au j-ieme élément de la permutation num[i] du paquet i
    return concat #liste de G.nbr éléments qui a un sommet i de G associe un sommet concat[i] de H
        
def recherche_isom(G, H, triG, triH): #tri une partition de [1,n]
    tailles_paquets = [len(ti) for ti in triG] #liste de la taille des paquets
    tri_imax = [fact(n)-1 for n in tailles_paquets] #liste du nombre de permutations par paquet #/!\ fact(n) - 1
    nmax = max(tailles_paquets) #taille du plus gros paquet
    p = permut_dynamique(nmax) #tableau fixe d'élément k ayant la liste des permutations de [1,k] (k e [0,nmax])
    t = len(triG)
    num, i = [-1]+[0]*(t-1), 0
    while i<t:
        if num[i]<tri_imax[i]:
            num[i] += 1
            #traitement
            x = test_isomorphism(G, H, concatenation(num, triG, triH, t, tailles_paquets,p) )
            if x != (False, []):
                return x
            #fin traitement
            i = 0
        while i<t and num[i]==tri_imax[i]:
            num[i] = 0
            i += 1
    return False, []
            
def isomorphism_tri(G,H,triG,triH):
    if G.nbr != H.nbr:
        return False, []
    if [len(e) for e in triH] != [len(e) for e in triG]:
        return False, []
    return recherche_isom(G, H, triG, triH)

#McKay

#partition des sommets sn -> partition equitable des sommets R(s) (cf mckay's canonical graph labeling)

def deg(G,w,V): #G un graphe, w un sommet de G, V une partie de G (partie de [|0,n-1|])
    degV = 0
    for x in G.connect[w]:
        if x in V:
         degV += 1
    return degV

def shatters(G,Vj,Vi): #Vj shatters Vi
    nvi = len(Vi)
    for k in range(nvi-1):
        for l in range(k+1,nvi):
            if deg(G,Vi[k],Vj) != deg (G,Vi[l],Vj):
                return True
    return False

def shattering(G,Vi,Vj): #shattering of Vi by Vj / on suppose shatters(G,Vj,Vi) / renvoie X=[X1,..,Xt] partition de Vi triés selon le degré dans Vj
    X = [[] for i in range(len(Vj)+1)] #au maximum, le degré d'un sommet de Vi dans Vj est len(Vj)
    for u in Vi:
        if deg(G,u,Vj) > len(Vj):
            print('u = ',u,' ; Vj = ',Vj,' ; deg = ' ,deg(G,u,Vj),' ; len(Vj) = ', len(Vj))
            print([x for x in G.connect[u] if x in Vj])
        X[ deg(G,u,Vj) ].append(u)
    return [x for x in X if x != []]
    
def refinement(G,s): #s=[V0,V1,...] une partition de [|0,n-1|], renvoie R(s) une partition équitable, propager l'information du degré ( cf part.4 mckay's canonical graph labeling )
    Rs = s.copy()
    B = [(i,j) for i in range(len(Rs)) for j in range(len(Rs)) if shatters(G,Rs[j],Rs[i])]
    im, jm = 0, 0
    while B!=[]:
        im, jm = min_couples(B)
        Rs = Rs[:im] + shattering(G,Rs[im],Rs[jm]) + Rs[im+1:]
        B = [(i,j) for i in range(len(Rs)) for j in range(len(Rs)) if shatters(G,Rs[j],Rs[i])]
    return Rs

#relation d'ordre sur les graphes, nombre binaire donné par l'ordre lexicographique des arêtes

def str_is(G,i,j):
    if j in G.connect[i] or i in G.connect[j]:
        return '1'
    return '0'

def i(G): #binary sequence of G
    bin = ''
    for i in range(G.nbr-1):
        for j in range(i+1,G.nbr):
            bin += str_is(G,i,j)
    return ''.join(bin)

def plus_grand_iG(iG,iH):
    if iG == '':
        return True
    elif iG[0]=='1' and iH=='0':
        return True
    elif iG[0]=='0' and iH=='1':
        return False
    else:
        plus_grand(iG[1:],iH[1:])
    

def plus_grand_v1(G,H):
    return plus_grand(i(G),i(H))

def plus_grand_v2(G,H): #i(G) et i(H) calculés au fur et à mesure, arrêt selon  ordre lexico
    for i in range(G.nbr-1):
        for j in range(i+1,G.nbr):
            g, h = int(str_is(G,i,j)), int(str_is(H,i,j))
            if g != h:
                return g and not h
    return True

def max_graphes(G, l_permut):
    intn = [i for i in range(G.nbr)]
    maxi, sigma_max = G, l_permut[0]
    for sigma in l_permut:
        adj_permut = [[] for _ in range(G.nbr)]
        for i in range(G.nbr):
            adj_permut[sigma[i]] = [sigma[e] for e in G.connect[i]]
        G_temp = Graph(intn,adj_permut)
        if plus_grand_v2(G_temp,maxi):
            maxi, sigma_max = G_temp, sigma
    return maxi, sigma_max
    

#search tree

class Tree:
  def __init__(self, val = None):
    self.node = val
    self.list = None

def leaf(T): #renvoie liste des feuilles
    l = []
    pile = [T] # parcours en profondeur
    while pile != []:
        t = pile.pop()
        if t.list==None:
            l.append(t.node)
        else:
            for tt in t.list:
                pile.append(tt)
    return l

def first_part(s): #renvoie la première partie non triviale de la partition s
    for i in range(len(s)):
        if len(s[i])>1:
            return i
    return -1
                 
def fils(G,t,affichage_arbre=False): #t un noeud
    s, u = t
    if len(s)==G.nbr:
        return None
    i = first_part(s)
    l_fils = []
    for ui in s[i]:
        R = refinement(G,s[:i] + [[ui],[x for x in s[i] if x!=ui]] + s[i+1:])
        if affichage_arbre:
            print((R, u+[ui]))
        l_fils.append( Tree((R, u+[ui])) )  
    return l_fils

def incrementer(G,T):
    if T.list==None:
        f = fils(G,T.node)
        T.list = f
        return f!=None
        
    else:
        continu = False
        for t in T.list:
            if incrementer(G,t):
                continu = True
        return continu 
        
def search_tree(G, s): #search tree dont la racine est ( s=(V1|V2|...), [] ), à chaque étage les fils sont (s perpend u) pour u dans V_i, V_i la première partie diff d'un singleton (cf mckay's...)
    T = Tree((refinement(G,s),[]))
    continu = True
    while continu:
        continu = incrementer(G,T)
    return T

def permutations_tree(G, s):
    l = leaf(search_tree(G,s))
    return [[singleton[0] for singleton in x[0]] for x in l]

def Cm(G,s=[]):
    if s==[]:
        s = [[i for i in range(G.nbr)]]
    l_permut = permutations_tree(G,s)
    return max_graphes(G, l_permut)

def isomorphes_mckay(G,H,sg=[],sh=[]):
    CmG, CmH = Cm(G,sg), Cm(H,sh)
    return (CmG[0].connect == CmH[0].connect), CmG[1], CmH[1]

def isomorphes_feuilles(G,H,sg=[],sh=[]):
    l_permut_G = permutations_tree(G,sg)
    l_permut_H = permutations_tree(H,sh)
    for i in range(len(l_permut_G)):
        if test_isomorphism2(G,H,l_permut_G[i],l_permut_G[i]):
            print( test_isomorphism2(G,H,l_permut_G[i],l_permut_G[i]) )
            return True, []
    return False, []

    
        





