from os import makedirs, listdir
import zipfile
import shutil
from distutils import dir_util

t = "\\begin{tcolorbox} \n \\prompt{In}{incolor}{ }{\\boxspacing} \n\\begin{Verbatim}[commandchars=\\\{\}] \n\PY{l+s+sd}{\PYZsq{}\PYZsq{}\PYZsq{}begin|On dÃƒÂ©finit un type de graphe particulier : d\PYZsq{}ordinaire notÃƒÂ© G(X,U) avec X l\PYZsq{}ensemble de sommets et U l\PYZsq{}ensemble des relations,} \n\PY{l+s+sd}{on considÃƒÂ¨re G\PYZsq{}(X) = G(X,U) avec U l\PYZsq{}ensemble des relation entre tous les sommets du graphe non\PYZhy{}orientÃƒÂ©.} \n\PY{l+s+sd}{On notera G\PYZsq{} = Graphepoints|end\PYZsq{}\PYZsq{}\PYZsq{}} \n\end{Verbatim} \n\end{tcolorbox} \n"

def record_file(c , text):
    makedirs('Customtex', exist_ok = True)
    name = str(c) + '.py'
    file_python = open(name, 'w' , encoding='utf8')
    file_python.write( text )
    file_python.close()
    
def removeboxes(line):
    out = ''
    if '\prompt' in line:
        out = '% ' + line
    else:
        out = line
    return out

def boxe2text(content):
    if not '\PYZsq{}\PYZsq{}\PYZsq{}begin|' in content:
        return content
    else:
        content = content.split('\PYZsq{}\PYZsq{}\PYZsq{}begin|')[1]
        content = content.split('|end\\PYZsq{}\\PYZsq{}\\PYZsq{}')[0]
        content = replace(content, '\PYZhy{}', '-')
        content = replace(content, '} \n\\PY{l+s+sd}{', ' ')
        content = replace(content, '}\n\\PY{l+s+sd}{', ' ')
        content = replace(content, '}\n\PY{l+s+sd}{', ' ')
        content = replace(content, '} \n\PY{l+s+sd}{', ' ')
        content = replace(content, '\PYZsq{}', '\'')
        content = replace(content, 'ÃƒÂ©', 'é')
        content = replace(content, 'ÃƒÂ¨', 'è')
        return content
        
def replace(line, str1, str2):
    return str2.join( line.split(str1) )

def red2blue(line):
    return replace(line, 'PY{c+c1}','PY{l+s+s1}')

def modifline(line):
    return removeboxes( red2blue(line) )

def modiffile( fichier, cible , nom ):
    makedirs(cible, exist_ok = True)
    new_fichier = open( (cible + '/' + nom), 'w', encoding='utf8')
    modifok = False
    for line in fichier:
        if modifok and (not '\\begin{tcolorbox}' in line) and (not '\\end{tcolorbox}' in line):
            new_line = modifline(line)
            new_fichier.write(new_line)
        else:
            if '\\begin{tcolorbox}' in line:
                modifok = True   
            if '\\end{}' in line:
                modifok = False
            new_fichier.write(line)
    new_fichier.close() 
    
def modifbloc( fichier, cible , nom ):
    makedirs(cible, exist_ok = True)
    new_fichier = open( cible+'/'+nom, 'w', encoding='utf8')
    modifok = False
    boxescontent = ''
    for line in fichier:
        if modifok:
            if '\\end{tcolorbox}' in line:
                modifok = False
                new_fichier.write( boxe2text(boxescontent) )
                new_fichier.write( line )
                boxescontent = ''
            else:
                boxescontent += line
        elif '\\begin{tcolorbox}' in line:
            modifok = True
            boxescontent = '\\begin{tcolorbox}'      
        else:
            new_fichier.write(line)
    new_fichier.write( boxescontent )
            
def modiftot(fichier, cible , nom):
    modiffile( fichier, cible, nom+'temp')
    with open( cible + '/' + nom + 'temp', 'r' ) as fichier2:
        modifbloc( fichier2, cible, nom)
            
#on veut à partir du dossier jupytertex, créer le dossier Customtex qui copie jupytertex puis modifie les fichiers tex qu'il contient
                
def copie():
    dir_util.copy_tree( 'C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\jupytertex', 'C:\\Users\\Adrien Dubois\\Desktop\\TIPE\\Customtex')
    
def modif():
    lzip = listdir('jupytertex')
    for fzip in lzip:
        name = fzip.split('.zip')[0]
        shutil.unpack_archive('jupytertex/'+fzip,'jupytertex/unpacked/'+name)
        shutil.copyfile('jupytertex/unpacked/'+name+'/'+name+'.tex', 'jupytertex/unpacked/'+name+'.tex')
        with open('jupytertex/unpacked/'+name+'.tex', 'r') as fichier:
            modiftot(fichier, 'jupytertex/unpacked/'+name, name+'.tex')
            shutil.make_archive('jupytertex/unpacked/zipmodif/'+name, 'zip', 'jupytertex/unpacked/'+name)
    dir_util.copy_tree( 'jupytertex/unpacked/zipmodif', 'Customtex')
    shutil.rmtree('jupytertex/unpacked')
    
modif()
#print( boxe2text( t ) )
    
        
        
        
            
            
    
    

    
        






