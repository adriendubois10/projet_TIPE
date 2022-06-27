#création d'une base de protéine basée sur une lecture (incomplète) de fichiers pdb

from os import listdir

path = 'C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\2-Code\\pdb'

l_pdb = [path+x for x in listdir(path) if '.pdb' in x]

print(l_pdb)

