from extract_PDB import *

#temp = gen_couvrant( filtre_nbr(read(pdb_ex),22), 0 )
#save(temp,'lim_22_1')
#temp = plier(permut_prot(temp))
#save(temp,'lim_22_2')

#sous-isomorphisme protéine

import sys
sys.path.insert(0, "anim2D")
from gencarbones2D import connexe

def filtre(prot,li):
    latom = [Atom(li.index(k), prot.latom[k].point, prot.latom[k].atom) for k in li]
    connect = [[li.index(v) for v in inter2(li,prot.connect[s])] for s in li]        
    return Protein(latom, connect)

def filtre_aretes(prot,lar):
    li = []
    for (i,j) in lar:
        if i not in li:
            li.append(i)
        if j not in li:
            li.append(j)
    latom, connect = [Atom(li.index(k), prot.latom[k].point, prot.latom[k].atom) for k in li], [[] for _ in li]
    for s in li:
        for v in prot.connect[s]:
            if ((s,v) in lar or (v,s) in lar):
                connect[li.index(s)].append(li.index(v))       
    P = Protein(latom, connect)
    if len(connexe(P,True)) > 1:
        return Protein([],[])
    return P

def subgraph(pg,pH,lH,ng,nh): #pg une sous protéine de pG (attention pas les mêmes numérotations)
    partH = parties(nh,ng) #ensemble des parties à ng éléments de [|0,nh-1|]
    for part in partH:
        ph = filtre_aretes(pH, [lH[i] for i in part]) #restriction de pH
        if pH!=None:
            ism, sigma = isom_invariants(pg,ph) #test d'isomorphisme sur les 2 restrictions
            if ism:
                save(ph, 'ph')
                return True, [lH[i] for i in part]
    return False, []

def subgraph_aretes(pG,pH,lH,ng,nh,larg): #pG et pH les protéines completes
    s = filtre_aretes(pG,larg) #restriction de pG à la liste larg d'arêtes
    if s==None: #pas connexe -> en "plusieurs morceaux"
        return False, []
    return subgraph( s, pH, lH,ng,nh)
 
def search_sub(pG,pH):
    lG, lH = pG.liaisons_sans_doublons_indice(), pH.liaisons_sans_doublons_indice() #liste des liaisons
    ng, nh = len(lG), len(lH) #nombres de liaisons
    if pG.nbr > pH.nbr:
        return search_sub(pH,pG)
    for n in range(pG.nbr,0,-1): #nombre de liaisons de pG sélectionnées
        print(n)
        partG = parties(ng,n) #parties de n éléments de [|0,ng-1|]
        for part in partG:
            b, s = subgraph_aretes(pG, pH, lH, n, nh, [lG[i] for i in part]) #conservation des n arêtes séléctionnées
            if b: #b si il existe une sous-partie de pH (de n arêtes) isomorphe à la protéine pG réduite
                save(filtre_aretes(pG,[lG[i] for i in part]),'pg')
                return True, s
    return False, []   
    
def infos_sub(prot1,prot2):
    d = time()
    sub_b, ls = search_sub(prot1,prot2)
    return sub_b, ls, time()-d
    
     
#infos_tris(prot_ex_isom1,prot_ex_isom2)
#infos_mckay(prot_ex_isom1,prot_ex_isom2,True)

prot22_1, prot22_2 = recup('lim_22_1'), recup('lim_22_2')

laretesG = [(1, 0), (2, 0), (3, 2), (4, 2), (5, 2), (6, 0), (7, 6), (8, 7), (9, 8), (10, 7), (11, 10), (12, 6), (13, 7), (14, 10), (15, 10), (16, 8), (17, 16), (18, 17), (19, 18), (20, 17)]
laretesH = [(1, 0), (2, 0), (3, 2), (4, 2), (5, 2), (6, 0), (7, 6), (8, 7), (9, 8), (10, 7), (11, 10), (12, 6), (13, 7), (14, 10), (15, 10), (16, 8), (17, 16), (18, 17), (19, 18), (20, 17)]
# pg_art = filtre_aretes(prot22_1, laretesG)
# ph_art = filtre_aretes(prot22_2, laretesH)
# save(pg_art,'pg_art')
# save(ph_art,'ph_art')

#print(isom_invariants(pg_art,ph_art))

#print(infos_sub(prot22_1, prot22_2))
#infos_tris(pg,ph)

#coeff

from cas_simple_nuage import *

def coeff_prox(ssp1,ssp2): #2 protéines supposées isomorphes, renumérotées selon la permutation, de même sommets
    N1, N2 = alignement(ssp1,ssp2)
    return 100 * r_coeff7(N1,N2) #moyenne du coefficient des distances et angles

def coeff_struct(pG,pH,ssp):
    ng, nh, np = len(pG.liaisons_sans_doublons_indice()), len(pH.liaisons_sans_doublons_indice()), len(ssp.liaisons_sans_doublons_indice())
    print(ng, nh, np)
    return 100*(2*np)/(ng+nh)

def coeff_tot(pG,pH):
    b, r = search_sub(pG,pH)
    if not b:
        return 0
    spg, sph = recup('pG'), recup('pH')
    cp, cs = coeff_prox(spg, sph), coeff_struct(pG,pH,spg)
    print(cp, cs)
#     variance = (100 - cs)/2
#     c = cs - variance + 2*variance*(cp/100)
    return (cs + cp)/2

p1 = recup('lim_22_1')
p2 = recup('lim_22_2')

print(coeff_tot(p1,p2))
    
        
    
    




    
    





