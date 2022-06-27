from geometrie_et_aux import *
from graphisomorphism import *
from time import time

class Atom:
    
    def __init__(self, i, position, atom): #par defaut i est l'indice dans la liste latom
        self.indice = i
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.point = position
        self.atom = atom
        
class Protein:
    
    def __init__(self, latom, connections): #connexions liste de taille len(latom) où connexions[i] est une liste des indices des molecules connectées
        self.latom = latom
        self.liste = [atom.point for atom in self.latom]
        self.nbr = len(latom)
        self.connect = [sans_repet_tri(c) for c in connections]
    
    def voisins(self, i):
        return self.connect[i]
    
    def ldegre(self):
        return [len(self.voisins(i)) for i in range(self.nbr)]
    
    def sort_by_degre(self): #liste tq l[i] ensemble des sommets de degre i
        ldeg = self.ldegre()
        return [ [s for s in range(self.nbr) if ldeg[s]==i] for i in range(max(ldeg)+1) ]
    
    def matrice_dist(self):
        mat = [[0]*self.nbr for _ in range(self.nbr)]
        for i in range(self.nbr):
            for j in range(i+1,self.nbr):
                mat[i][j] = distance(self.latom[i].point, self.latom[j].point)
                mat[j][i] = mat[i][j]
        return mat
    
    def extraire_molecule(self, at):
        return [self.latom[i] for i in range(self.nbr) if self.latom[i].atom == at]
    
    def enum_molecule(self, atom): #renvoie un dictionnaire
        num_atom = {}
        for m in self.latom:
            if not m.atom in s:
                num_atom[ m.atom ] = 0
            num_atom[ m.atom ] += 1
        return num_atom
            
    def liaisons_sans_doublons(self):
        def maxi(liste):
            if liste==[]:
                return 0
            return max(liste)
        def rev(couple):
            a,b=couple
            return b,a
        lcouples = [ (self.latom[i],self.latom[j]) for i in range(self.nbr) for j in self.connect[i] ]
        n, k = len(lcouples), 0
        while k < n:
            if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
                lcouples.pop(k)
                n += -1
            else:
                k += 1
        return [(m1.point,m2.point) for (m1,m2) in lcouples]
    
    def liaisons_sans_doublons_indice(self):
        def maxi(liste):
            if liste==[]:
                return 0
            return max(liste)
        def rev(couple):
            a,b=couple
            return b,a
        lcouples = [ (i,j) for i in range(self.nbr) for j in self.connect[i] ]
        n, k = len(lcouples), 0
        while k < n:
            if (lcouples[k] in lcouples[k+1:]) or (rev(lcouples[k]) in lcouples[k+1:]):
                lcouples.pop(k)
                n += -1
            else:
                k += 1
        return lcouples
    
#prot -> graphe (perte d'infos)
    
def graph_of_prot(prot):
    return Graph([i for i in range(prot.nbr)], prot.connect)

#verifier le tri

def verif(G,tri):
    for i in range(G.nbr):
        if not (True in [(i in t) for t in tri]):
            return False
    return True
    
#tri des sommets pour une protéine
   
def sort_by_deg_atom(prot): #proposition d'un tri canonique par degre et type d'atome
    G = graph_of_prot(prot)
    ld = G.sort_by_degre()
    la = []
    for at in ['C','N','O','H','S']:
        l = []
        for i in range(prot.nbr):
            if prot.latom[i].atom == at:
                l.append(i)
        la.append( l )
    la = [l for l in la if l!=[]]
    return assoc_canonique([ld,la]) #on combine les caractéristiques degre et type

#test d'isomorphisme tri

def isom_invariants(prot1,prot2):
    if prot1.nbr==0 or prot2.nbr==0:
        return False, []
    G, H = graph_of_prot(prot1), graph_of_prot(prot2)
    triG, triH = refinement(G,sort_by_deg_atom(prot1)), refinement(H,sort_by_deg_atom(prot2))
    isom = isomorphism_tri(G, H, triG, triH)
    return isom

#test d'isomorphisme mckay

def isom_mckay(prot1,prot2):
    d = time()
    if prot1.nbr==0 or prot2.nbr==0:
        return False, 0
    G, H = graph_of_prot(prot1), graph_of_prot(prot2)
    sg, sh = sort_by_deg_atom(prot1), sort_by_deg_atom(prot2)
    isom = isomorphes_mckay(G,H,sg,sh)
    return isom, time()-d

def isom_mckay_feuilles(prot1,prot2):
    d = time()
    G, H = graph_of_prot(prot1), graph_of_prot(prot2)
    sg, sh = sort_by_deg_atom(prot1), sort_by_deg_atom(prot2)
    isom = isomorphes_feuilles(G,H,sg,sh)
    return isom, time()-d
    


    











