from def_protein import *
from generer_protein import *

#lecture pdb

def entier(car):
    car = car.split('.')
    a, b = int(car[0]), int(car[1])
    return round( a + b/10**len(car[1]), 2)
            
def read(pdb, liaisons=False):
    file = open(pdb)
    li, lp, lm, connect = [], [], [], []
    for line in file:
        if ('ATOM' in line) or ('HETATM' in line):
            l = [x for x in line.split(' ') if x!='' and (x!='\n') and (x!='\\n') and (x!="'\n")]
            if l[0]=='ATOM' or l[0]=='HETATM':
                li.append( int(l[1]) )
                point = [entier(l[6]),entier(l[7]),entier(l[8])]
                lp.append(point)
                lm.append(l[-1])
        if 'CONECT' in line:
            connect.append([int(y) for y in [x for x in line.split(' ') if (x!='') and (x!='CONECT') and (x!='\n') and (x!='\\n') and (x!="'\n")]])
    file.close()
    for k in range(len(connect)): #Renumérotation
        for l in range(len(connect[k])):
            connect[k][l] = li.index(connect[k][l])
    if liaisons:
        connexions = [[] for _ in range(len(li))]
        for c in connect:
            connexions[c[0]] = c[1:]
        P = Protein([Atom(k,lp[k],lm[k]) for k in range(len(li))], connexions) #connexions ne fonctionne pas -> subtilités du format
        return filtre_RE(P)
    P = Protein([Atom(k,lp[k],lm[k]) for k in range(len(li))], [[] for _ in range(len(li))]) #sans connections
    return filtre_RE(P)

def test(pdb):
    file = open(pdb)
    for line in file:
        print(line)
        
#écrire
        
save_folder = "C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\2-Code\\pdb\\save_prot\\"

def concatstr(liste):
    s = ''
    for l in liste:
        s += str(l)+' '
    return s

def save(prot,nom):
    file = open(save_folder + nom, 'w')
    file.write('latom\n')
    for at in prot.latom:
        file.write(str(at.indice) +';'+ concatstr(at.point) +';'+ str(at.atom)+'\n')
    file.write('connect\n')
    for i in range(prot.nbr):
        file.write(concatstr(prot.connect[i])+'\n')
    file.close()
    
def recup(nom):
    file = open(save_folder + nom, 'r')
    latom, connect = [], []
    blat, bcon = False, False
    for line in file:
        if 'latom' in line:
            blat = True
        elif 'connect' in line:
            blat, bcon = False, True
        elif blat:
            i, p, a = tuple(line.split(';'))
            i, a =  int(i), a[0]
            p = [float(k) for k in (p.split(' ')) if k!='']
            latom.append( Atom(i,p,a) )
        elif bcon:
            l = line.split(' ')[:-1]
            connect.append([int(k) for k in l])
    return Protein(latom, connect)
                   
#créer les exemples pour la présentation

pos1 = {1: (0, 0), 2: (1,0), 3: (2,1), 4: (1,2), 5: (0,2), 6: (-1,1)}
pos2 = {1: (0,2), 2: (0.9,1.4), 3: (1.5,0.5), 4: (2,2), 5: (2.5,1), 6: (1,-1)}

def adj(lar):
    m = max([max(c) for c in lar])
    adja = [[] for _ in range(m)]
    for (i,j) in lar:
        adja[i-1].append(j-1)
        adja[j-1].append(i-1)
    return m, adja

n1, S1 = adj([(1,4),(1,6),(1,2),(2,5),(2,3),(3,6),(3,4),(4,5),(5,6)])
n2, S2 = adj([(1,2),(1,4),(1,6),(2,3),(2,5),(3,4),(3,6),(4,5),(5,6)])

tat1 = ['C','H','C', 'C', 'H','C']
tat2 = ['O','C', 'H', 'H', 'N','S']
lat1 = [Atom(i,(*pos1[i+1],np.random.random()),tat1[i]) for i in range(n1)]
lat2 = [Atom(i,(*pos2[i+1],np.random.random()),tat1[i]) for i in range(n1)]
lat3 = [Atom(i,(*pos2[i+1],np.random.random()),tat2[i]) for i in range(n1)]
prot_isom1 = Protein(lat1,S1)
prot_isom2 = Protein(lat2,S2)
prot_isom3 = Protein(lat3,S2)

nr, Sr = adj([(1,4),(2,4),(4,5),(3,5)])
posr = {1: (0, 0), 2: (2,0), 3: (4,0), 4: (1,2), 5: (3,2)}
tatr = ['O','O','C','O','C']
latr = [Atom(i,(*posr[i+1],np.random.random()),tatr[i]) for i in range(nr)]
prot_tri1 = Protein(latr,Sr)
nt, St = adj([(1,4),(2,4),(4,5),(3,5)])
post = {1: (-2, 6), 2: (2,6), 3: (0,0), 4: (0,4), 5: (0,2)}
latt = [Atom(i,(*post[i+1],np.random.random()),tatr[i]) for i in range(nr)]
prot_tri2 = Protein(latt,St)

#test pour isomorphisme

pdb_ex = "C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\2-Code\\pdb\\prot1.pdb "

def gen_isom_prot(liaisons_supp=0.1,replace=False):
    new_prot_ex_isom1 = gen_couvrant(read(pdb_ex),liaisons_supp)
    new_prot_ex_isom2 = plier(permut_prot(new_prot_ex_isom1))
    if replace:
        save(new_prot_ex_isom1,'prot_ex_isom1')
        save(new_prot_ex_isom2,'prot_ex_isom2')
    else:
        save(new_prot_ex_isom1,'prot_ex_isom1prime')
        save(new_prot_ex_isom2,'prot_ex_isom2prime')
        
#exemples proteines
        
prot_ex_isom1 = recup('prot_ex_isom1')
prot_ex_isom2 = recup('prot_ex_isom2')

#base de protéines
        
from os import listdir
from generer_protein import *

path = 'C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\2-Code\\pdb'
l_pdb = [path+'\\'+x for x in listdir(path) if '.pdb' in x]
l_prot = [gen_couvrant(read(pdb),0.1) for pdb in l_pdb]


        

              