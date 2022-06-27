# I] generer protein à partir d'une lecture incomplète de pdb /!\ pas de prise en compte du nbr de liaisons par atomes (C -> 4 liasons etc)
    
def generer_liaisons_carbones(prot):
    ''' Entrée : Une protéine avec ou sans liaisons
        Sortie : Une protéine munie de liaisons carbones générées de proche en proche'''
    
    conect = [[] for _ in range(prot.nbr)]
    carbones = Protein(prot.extraire_molecule('C'), [])
    nc = carbones.nbr
    matdist = matrice_dist(carbones.liste)
    
    Rmin = min( [min(matdist[i])  for i in range(nc)] ) /4 #div par 2 car passage de diamètre a dist puis par 2 car les rayons vont augmenter en mm temps
    pas = ecart_type(matdist[0][1:])/(nc-1) #ecart-type des rayons sur le nbr de rayons -> au lieu de (max-min) permet de ne pas perdre en précision si un seul atome est très éloigné
    lrayons = [Rmin]*nc
    rayonsfixes = [False]*nc
    
    while False in rayonsfixes:
        for i in [i for i in range(nc) if rayonsfixes[i]==False]:
            for j in [j for j in range(nc) if j!=i]:
                if lrayons[i]+lrayons[j] >= matdist[i][j]:
                    rayonsfixes[i],rayonsfixes[j] = True, True
                    matdist[i][j], matdist[j][i] = True, True #les distances ne serviront plus, pr preserver memoire utilisation matrice pr stocker liaisons
        for i in [i for i in range(nc) if rayonsfixes[i]==False]:
            lrayons[i] += pas
    for i in range(nc):
        for j in range(nc):
            if matdist[i][j]==True: #attention peut contenir des reels
                conect[carbones.latom[i].indice].append(carbones.latom[j].indice) #réindexation pour l'ajout des liaisons C-C à l'ensemble des atomes
    return Protein(prot.latom, conect)
        
def normeinf(atom, squelette): #cf generer_ON
        d = [distance(atom.point,s.point) for s in squelette]
        dmin = min(d)
        return dmin, d.index(dmin)
    
def generer_ON(protc):
    squelette = protc.extraire_molecule('C')
    connect = protc.connect
    #idée : on cherche le O ou N le plus proche du squelette, puis on l'ajoute au squelette en le reliant au sommet le plus proche
    #itérer jusqu'à avoir traité tous les O et N
    ON = protc.extraire_molecule('O') + protc.extraire_molecule('N')
    while ON != []:
        l = [normeinf(a, squelette) for a in ON]
        iON = indice_min([x[0] for x in l])
        iS = l[iON][1]
        atom = ON.pop(iON)
        squelette.append(atom)
        connect[atom.indice].append(iS)
        connect[iS].append(atom.indice)
    return Protein(protc.latom, connect)

def generer_H(prot_CON):
    H = prot_CON.extraire_molecule('H')
    squelette = prot_CON.extraire_molecule('C')+prot_CON.extraire_molecule('O')+prot_CON.extraire_molecule('N')
    connect = prot_CON.connect
    for h in H:
        iS = normeinf(h, squelette)
        connect[ squelette[iS[1]].indice ].append(h.indice)
        connect[ h.indice ].append(squelette[iS[1]].indice)
    return Protein( prot_CON.latom, connect )
        

def generer_liaisons(prot): #generer les liaisons d'une proteine a partir de la liste des atomes
    return generer_H( generer_ON ( generer_liaisons_carbones(prot) ))
        
    
            
    #objectif : 2 à 3 voire 4 laisons max par atome, vider la liste des connexions ?
    
    #relier carbones de proches en proches('cahine principale)
    #carbones restants à relier au carbone le plus proche de la chaine
    
    #supprimer hydorgènes -> résidus non visibles au rayons X
    #chaines secondaires reliées à un carbone passant par les molécules non visitées de proches en proches
    
    #pour les atomes restants
