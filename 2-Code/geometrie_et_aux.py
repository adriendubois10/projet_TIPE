import numpy as np
import random as rd

#divers

def fact(n):
    k = 1
    for i in range(2,n+1):
        k = k*i
    return k

def permutations(n): #liste des permutations d'un ensemble [0,1,...,n-1]
    if n<=1:
        return [[0]]
    pm, l = permutations(n-1), []
    for i in range(len(pm)+1):
        for p in pm:
            l.append( p[:i] + [n-1] + p[i:] )
    return l

def permutliste(seq, er=False): #permutations non récursif, er=False si pas de répétition
    p = [seq] 
    n = len(seq)
    for k in range(n):
        for i in range(len(p)):
            z = p[i][:]
            for c in range(n-k):
                z.append(z.pop(k))
                print(z)
                if er==False or (z not in p):
                    p.append(z[:])
    return p

def permut_dynamique(n): #renvoie la liste des permutation de 0:[] à n
    permut = [ [] , [[0]], ]
    for k in range(2,n+2):
        l  = []
        lm = len(permut[k-1])
        for i in range(lm+1):
            for p in permut[k-1]:
                l.append( p[:i] + [k-1] + p[i:] )
        permut.append(l)
    return permut

def permut_dyn_liste(p, l): #p = permut_dynamique(n) avec len(l)<=n
    k = len(l)
    return [[l[i] for i in f] for f in p[k]] #on applique la permutation à la liste    

def indice_min(l, value=False):
    n = len(l)
    mini, i0 = l[0], 0
    for i in range(n):
        if l[i] < mini:
            mini, i0 = l[i], i
    if value:
        return i0, mini
    return i0

def indice_max(l, value=False):
    n = len(l)
    maxi, i0 = l[0], 0
    for i in range(n):
        if l[i] > maxi:
            maxi, i0 = l[i], i
    if value:
        return i0, maxi
    return i0

def privede(l1, l2):
    return [x for x in l1 if not x in l2]

def numerotation(l):
    t, num, i = len(l), [-1]+[0]*(t-1), 0
    while i<t:
        if num[i]<l[i]:
            num[i] += 1
            #traitement
            i = 0
        while i<t and num[i]==l[i]:
            num[i] = 0
            i += 1
            
#parties
            
def parties(n,k): #liste des parties à k éléments de [|0,n-1|] (même ordre)
    num, i, s, part = [-1]+[0]*(n-1), 0, -1, [] #s est la somme de num
    while i<n:
        if num[i]<1:
            num[i] += 1
            s += 1
            if s==k:
                part.append( [i for i in range(n) if num[i]] )
            i = 0
        while i<n and num[i]==1:
            num[i] = 0
            s+= -1
            i += 1
    return part
              
def sans_repet(l):
    return [l[i] for i in range(len(l)) if not (l[i] in l[i+1:])]

def sans_repet_tri(l):
    if l==[]:
        return []
    n = max(l)+1
    lind = [False]*n
    for x in l:
        lind[x] = True
    return [i for i in range(n) if lind[i]]

def doublon(l): #bool, unicité des termes de l
    for i in range(len(l)-1):
        if l[i] in l[i+1:]:
            print(l[i], l[i+1:])
            return True
    return False   
    
def min_couples(lcouples): #ordre lexicographique / non vide
    def plus_petit(e,f):
        (a,b),(c,d) = e,f
        return a<c or (a==c and b<=d)
    cmin = lcouples[0]       
    for x in lcouples:
        if plus_petit(x,cmin):
            cmin = x
    return cmin
 
#opérations sur les permutations

def inverse(sigma):
    n = len(sigma)
    sigma_inv = [0]*n
    for i in range(n):
        sigma_inv[sigma[i]] = i
    return sigma_inv

def composee(sigma2,sigma1):
    return [ sigma2[sig1] for sig1 in sigma1 ]

#geometrie en 3 dimensions

def distance(A,B):
    return np.sqrt( abs(A[0]-B[0])**2 + abs(A[1]-B[1])**2 + abs(A[2]-B[2])**2 )

def angle(ab,ac,bc): #angle en B en radians
    x = (ab**2 + bc**2 - ac**2) / (2*ab*bc)
    return np.arccos(x)

def orientertriangle(A,B,C,ld): #renvoie les points dans l'ordre base,coté1,cote2 et ld=[dab,dac,dbc]
    dmax, i0 = 0, 0
    if ld[0]>ld[1] and ld[0]>ld[2]:
        pass
    elif ld[1]>ld[0] and ld[1]>ld[2]:
        i0 = 1
    else:
        i0 = 2
    return [(A,B,C), (A,C,B), (B,C,A)][i0], [ ld, [ld[1],ld[2],ld[0]], [ld[2],ld[0],ld[1]] ][i0]         
    
def airetriangle(A,B,C):
    (A,B,C), ld = orientertriangle( A,B,C, [distance(A,B),distance(A,C),distance(B,C)] )
    ab, ac, bc = tuple(ld)
    alpha = angle(ab,ac,bc)
    h = bc * np.sin(alpha)
    base = ab
    return 0.5 * base * h

def airepoly(A,B,C,D):
    return airetriangle(A,B,C) + airetriangle(D,B,C)

def matrice_dist(l): #liste de coordonnées
    n = len(l)
    mat = [[0]*n for _ in range(n)]
    for i in range(n):
        for j in range(i+1,n):
            mat[i][j] = distance(l[i],l[j])
            mat[j][i] = mat[i][j]
    return mat

def translation(prot, vect):
    for i in range(ssp1.nbr):
        prot.liste[i] = [ prot.liste[i][k]-vect[k] for k in [0,1,2] ]
        
def rotation(ssp2, theta, u):
    u = (1/np.numpy.linalg.norm(u,2)) * u
    ux, uy, uz = tuple([u[k] for k in [0,1,2]])
    P = np.array( [ [ux**2, ux*uy, ux*uz], [ux*uy, uy**2, uy*uz], [ux*uz, uy*uz, uz**2] ])
    I = np.identity(3)
    Q = np.array( [[0, -uz, uy], [uz, 0, -ux], [-uy, ux, 0]] )
    R = P + np.cos(theta) * (I - P) + np.sin(theta) * Q
    for i in range(ssp1.nbr):
        D = np.dot( R, np.array( prot.liste[i] ) )
        prot.liste[i] = [D[k] for k in [0,1,2]]
    
def alignement_translation(ssp1,ssp2):
    offset_moy = [0,0,0]
    for i in range(ssp1.nbr):
        offset_moy = [offset_moy[k] - (1/ssp1.nbr)*(N2[i][k] - N1[i][k]) for k in [0,1,2]]
    translation(ssp2, offset_moy)

def alignement_rotation(ssp1,ssp2):
    translation(ssp2, [ ssp1.liste[i][k]-ssp2.liste[i][k] for k in [0,1,2] ] ) #1ers atomes confondus
    theta1 = angle( *tuple( [ distance(A,B) for (A,B) in [(ssp1.liste[0],ssp1.liste[1]),(ssp1.liste[1],ssp2.liste[1]),(ssp2.liste[0],ssp2.liste[1])]]) )   
    u1 = np.cross(np.array(ssp1.liste[1])-np.array(ssp1.liste[0]), np.array(ssp2.liste[1])-np.array(ssp2.liste[0]))
    rotation(ssp2, theta1, u1) # alignement par rotation des 2e atomes
    d1 = distance(ssp1.liste[1],ssp1.liste[2])
    d2 = distance(ssp1.liste[2],[ssp2.liste[2][k]-(ssp2.liste[1][k]-ssp1.liste[1][k]) for k in range [0,1,2]])
    d3 = distance(ssp2.liste[1],ssp2.liste[2])
    theta2 = angle(d1, d2, d3)
    u2 = np.array(ssp1.liste[1])-np.array(ssp1.liste[0])
    rotation(ssp2, theta2, u2) #aligement par rotation des 3e atomes

def alignement(ssp1,ssp2): #2 protéines supposées isomorphes, renumérotées selon la permutation, de même sommets
    alignement_rotation(ssp1,ssp2)
    alignement_translation(ssp1,ssp2)
    N1, N2 = [ssp1.liste[0]],[ssp2.liste[0]]
    for i in range(1,ssp1.nbr-1):
        N1.append(ssp1.liste[i])
        N1.append(ssp1.liste[i])
        N2.append(ssp2.liste[i])
        N2.append(ssp2.liste[i])
    N1.append(ssp1.liste[-1])
    N2.append(ssp2.liste[-1])    
    offset_moy = [0,0,0]
    for i in range(ssp1.nbr):
        offset_moy = [offset_moy[k] + (1/ssp1.nbr)*(N2[i][k] - N1[i][k]) for k in [0,1,2]]
    return nuagepoints(N1), nuagepoints(N2)

#nuage_de_point

def distpoints(NA,NB):
    return [distance(NA.liste[i],NB.liste[i]) for i in range(NA.nbr)]

def dist_reset(NA,NB):
    D = [distance(NA.liste[0],NB.liste[0])]
    vecta = np.array([0.,0.,0.])
    vectb = np.array([0.,0.,0.])
    for i in range(NA.nbr-1):
        vecta += np.array(NA.liste[i+1]) - np.array(NA.liste[i])
        vectb += np.array(NB.liste[i+1]) - np.array(NB.liste[i])
        D.append( distance(np.array(NA.liste[i+1])-vecta, np.array(NB.liste[i+1])-vectb) )
    return D

def liste_angles(NA,NB):
    theta = []
    for i in range(NA.nbr-1):
        vect = np.array(NA.liste[i]) - np.array(NB.liste[i])
        new_A = np.array(NB.liste[i+1]) + vect
        d1 = distance( new_A, NA.liste[i])
        d2 = distance( new_A, NA.liste[i+1])
        d3 = distance( NA.liste[i], NA.liste[i+1] )
        theta.append( angle(d1,d2,d3) )
    return theta
        
def aires_liste(NA,NB):
    A = []
    for i in range(NA.nbr - 1):
        A.append( airepoly(NA.liste[i+1],NB.liste[i+1],NA.liste[i],NB.liste[i]) )
    return A

def aire(NA,NB):
    return sum( aires_liste(NA,NB) )

def color_dlines(dl): # entre 1 et 10
    n, m, M = len(dl), min(dl), max(dl)
    lcolor = [0 for _ in range(n)]
    for i in range(n):
        if dl[i]==m:
            lcolor[i] = 1
        else:
            lcolor[i] = int( np.ceil(10*(dl[i]-m) / (M-m)) ) - 1
    return lcolor

def rotation_z(liste,x=5,y=5,theta=-np.pi/2):
    r = np.array([[np.cos(theta), np.sin(theta),0], [np.sin(theta), np.cos(theta),0], [0,0,1]])
    ref = np.array([x, y, 0])
    def torefcolonne(i):
        return (np.array(i)-ref).reshape(3,1)
    N1 = [(ref + torefcolonne(point).reshape(1,3)).tolist()[0] for point in liste]
    return N1

def paramtriangle(u,v,A,B,C):
    O = np.array(A)
    v1 = np.array(B) - np.array(A)
    v2 = np.array(C) - np.array(A)
    if v <= (1-u):
        return O + u * v1 + v * v2
    return O + v2

#stats

def esperance(l):
    return sum(l)/len(l)

def variance(l):
    print(l)
    e1 = esperance([x**2 for x in l])
    e2 = esperance(l)**2
    return e1 - e2

def ecart_type(l):
    return np.sqrt(variance(l))