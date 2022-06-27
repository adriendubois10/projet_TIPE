from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from geometrie_et_aux import *
from mesure_Rcoeffs import *

#class

class nuagepoints:
    
    def __init__(self,l):
        self.nbr = len(l)
        self.liste = l
        self.x = [i[0] for i in l]
        self.y = [i[1] for i in l]
        self.z = [i[2] for i in l]
        self.bords = ( [min(self.x),min(self.y),min(self.z)], [max(self.x),max(self.y),max(self.z)] ) #coordonnées d'un pavé englobant les points
        self.dist = [distance(self.liste[i],self.liste[i+1]) for i in range(self.nbr-1)]
        self.len = sum(self.dist)
        self.diag = [np.dot(self.liste[i],[1,1,1])/np.sqrt(3) for i in range(self.nbr)]
    
    def write(self):
        for x in self:
            print(x[0], x[1], x[2])
            
    def show(self, relies=False): #points reliés : dans l'ordre de le liste
        fig = plt.figure()
        md = Axes3D(fig)
        for a in self.liste:
            md.scatter(a[0],a[1],a[2], linewidths = 4)
        if relies:
            for i in range(self.nbr - 1):
                md.plot(self.x[i:i+2],self.y[i:i+2],self.z[i:i+2], color='black')       
        plt.show()      
        
        
#exemple - nuage point (non lies / lies)
        
def rda(x=0.5,eps=0.5):
    a, b = x-eps, x+eps
    return (b-a)*rd.random() + a 
            
def generernuage(n=10,xlim=10,ylim=10,zlim=10):
    l = []
    for _ in range(n):
        l.append([xlim*rda(),ylim*rda(),zlim*rda()])
    return nuagepoints(l)

def genererliaisons(): #on trie les points selon la diagonale (axe n=(1,1,1) passant par O)
    g = generernuage()
    l = []
    for i in range(g.nbr):
        if l==[]:
            l.append([g.liste[i],g.diag[i]])
        else:
            for j in range(len(l)):
                if g.diag[i]<=l[j][1]:
                    l = l[:j] + [g.liste[i],g.diag[i]] + l[j:]
                    break
                if j==n:
                    l.append([g.liste[i],g.diag[i]])
        return nuagepoints([h[0] for h in l])
                    
def genererliaisonsunif(n, c):
    D = distance([0,0,0],[c, c, c]) #diagonale du cube
    ndiag = [k*(D/(n+1)) for k in range(1,n+1)]
    u = (1/np.sqrt(3)) * np.array( [-1,-1, 1])
    v = (1/np.sqrt(2)) * np.array( [ 1, -1, 0])
    
    def is_incube(l, c):
        return 0<=l[0]<=c and 0<=l[1]<=c and 0<=l[2]<=c    
    
    def genpointdiag(diag,M):
        while 1:
            x = M * (-1 + 2*rd.random())
            y = M * (-1 + 2*rd.random())
            A = ( diag/np.sqrt(3) * np.array([1,1,1]) )
            B = x * u
            C = y * v
            point = (A+B+C).tolist()
            if is_incube(point, c):
                return point     
            
    def interplancube(diag, c): #donne
        if diag <= D/np.sqrt(3) :
            x = diag * np.sqrt(3)
            return [ [x,0,0], [0,x,0], [0,0,x] ]
        elif diag >= D*(1-np.sqrt(3)) :
            x = c - (D-diag) * np.sqrt(3)
            return [ [x,c,c], [c,x,c], [c,c,x] ]
        return [ [c,0,0] ]
    def distM(diag, c): #definir un distance a la diagonale du cube maximale
        P = interplancube(diag, c)
        A = ( diag/np.sqrt(3) * np.array([1,1,1]) ).tolist()
        return max([distance(A,p) for p in P])
    
    l = []
    for i in range(n):
        M = distM(ndiag[i], c)
        l.append( genpointdiag(ndiag[i], M) )
        
    return nuagepoints(l)

def rot_z(N,x=5,y=5,theta=-np.pi/2):
    liste = N.liste
    lr = rotation_z(N.liste,x,y,theta)
    return nuagepoints(lr)
    

#exemple - générer une approximation a partir d'un modele

def decalagex(NA,eps,offset=0):
    l = []
    for i in range(NA.nbr):
        l.append( [NA.x[i], NA.y[i] + rda(0.1,1)*eps + offset, NA.z[i]] )
    return nuagepoints(l)
    
#affichage temporaire

N1 = generernuage()
N2 = genererliaisons()
N3 = genererliaisonsunif(10, 10)
N5 = genererliaisonsunif(10, 10)
N6 = decalagex(N3,1)
#N4 = rot_z(N1)

#Coefficients
        
def r_coeff1(NA,NB):
    return 1 / ( 1 + sum(distpoints(NA,NB))/NA.len ) #creuser ecart avec 1 -> passer sum... à une racine nieme

def r_coeff2(NA,NB):
    return 1 - sum(distpoints(NA,NB))/NA.len

def r_coeff3(NA,NB):
    return 1 / ( 1 + aire(NA,NB) / NA.len**2 )

def r_coeff4(NA,NB):
    return 1 / ( 1 + np.sqrt(aire(NA,NB)) / NA.len )

def r_coeff5(NA,NB):
    return (r_coeff4(NA,NB))**2

def r_coeff6(NA,NB):
    return (1 / ( 1 + sum(dist_reset(NA,NB))/NA.len) )

def r_coeff_dist(NA,NB):
    return  1/(1+ (sum([ abs(NA.dist[i] - NB.dist[i]) for i in range(NA.nbr - 1) ]) / max(NA.len,NB.len)))

def r_coeff_angles(NA,NB):
    theta = liste_angles(NA,NB)
    return 1/(1+(sum([ abs(np.sin(theta[i]/2)) * max(NA.dist[i],NB.dist[i]) for i in range(NA.nbr-1)]) / sum([max(NA.dist[i],NB.dist[i]) for i in range(NA.nbr-1)])))

def r_coeff7(NA,NB,k=2):
    return ( r_coeff_dist(NA,NB) + r_coeff_angles(NA,NB) ) / 2
    
#affichage

def show(N, M, relies=False): #points reliés : dans l'ordre de le liste
        fig = plt.figure()
        md = plt.axes(projection='3d')
        for a in N.liste:
            md.scatter(a[0],a[1],a[2], linewidths = 4, color='r')
        for a in M.liste:
            md.scatter(a[0],a[1],a[2], linewidths = 4, color='m')   
        if relies:
            for i in range(N.nbr - 1):
                md.plot(N.x[i:i+2],N.y[i:i+2],N.z[i:i+2], color='black')
                md.plot(M.x[i:i+2],M.y[i:i+2],M.z[i:i+2], color='blue')
        print('r1 = ',r_coeff1(N,M), '; r6 = ', r_coeff6(N,M))
        print('rdist = ',r_coeff_dist(N,M),'; rangle = ',r_coeff_angles(N,M), 'rcoeff7 = ',r_coeff7(N,M) )
        plt.show()


#show(N3,N6,True)
    
