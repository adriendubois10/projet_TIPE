from extract_PDB import *
        
#gen_isom_prot(0.1,False)
     
#gen_isom_prot()

def infos_tris(prot1,prot2,afficher_permut=False):
    deps = time()
    s1, s2 = sort_by_deg_atom(prot1), sort_by_deg_atom(prot2)
    arrs = time()
    G1, G2 = graph_of_prot(prot1), graph_of_prot(prot2)
    deprs = time()
    rs1, rs2 = refinement(G1,s1),refinement(G2,s2)
    arrrs = time()
    m = max([len(l) for l in s1])
    print('s1')
    for i in range(1,m+1):
        e = sum([len(l)==i for l in s1])
        if e!=0:
            print('{} : '.format(i), e)
    print('')
    print('rs1')
    m= max([len(l) for l in rs1])
    for i in range(1,m+1):
        e = sum([len(l)==i for l in rs1])
        if e!=0:
            print('{} : '.format(i), e)
    print('')
    print('tri deg/atom : ',arrs-deps,' ; refinement : ',arrrs-deprs)
    tri_ex = isom_invariants(prot1,prot2)
    if afficher_permut:
        print(tri_ex[1])
    print('isomorphes : ',tri_ex)
    
def infos_mckay(prot1,prot2,afficher_permut=False):
    #mckay_ex, t2 = isom_mckay(prot_ex_isom1,prot_ex_isom2)
    mckay_ex, t2 = isom_mckay_feuilles(prot_ex_isom1,prot_ex_isom2)
    if afficher_permut:
        print(mckay_ex[1])
    print('')
    print('ismorphes ',mckay_ex[0], t2)
    

