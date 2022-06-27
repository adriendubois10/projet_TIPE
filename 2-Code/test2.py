import numpy as np

class Atom:
    
    def __init__(self, i, position, atom):
        self.indice = i
        self.x = position[0]
        self.y = position[1]
        self.z = position[2]
        self.point = position
        self.atom = atom

class Cercle: #besoin d'une litse des indices des carbones
    def __init__(self,atome):
        self.atom = atome
        self.centre = atome.point
        self.rayon = 0
        self.fixe = False #False:=centre fixe pas rayon; i:=centre en translation par rapport au centre du cercle i; True:=fixe
        self.indice = atome.indice
        
    def trans_from(self,c,eps):
        v1 = np.array(self.centre)-np.array(c.centre)
        v = (1/np.linalg.norm(v1))*v1
        self.centre = ( np.array(self.centre) + (1+eps)*v ).tolist()
        self.rayon = self.rayon + eps
        
        
        
    def contact(self,c):
        return distance(self.centre,c.centre) <= (self.rayon + c.rayon)
    
a = Atom(0,[1,1,1],'C')
ce = Cercle(a)