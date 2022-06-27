from cas_simple_nuage import *

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

#exemple - générer une approximation a partir d'un modele

def decalagex(NA,eps):
    l = []
    for i in range(NA.nbr):
        l.append( [NA.x[i], NA.y[i] + rda(0.1,1)*eps, NA.z[i]] )
    return nuagepoints(l)
    
#affichage temporaire

N1 = generernuage()
N2 = genererliaisons()
N3 = genererliaisonsunif(10, 10)
N4 = rotation_z(N1)

def show(N, M, relies=False): #points reliés : dans l'ordre de le liste
        fig = plt.figure()
        md = Axes3D(fig)
        for a in N.liste:
            md.scatter(a[0],a[1],a[2], linewidths = 4)
        for a in M.liste:
            md.scatter(a[0],a[1],a[2], linewidths = 4)   
        if relies:
            for i in range(N.nbr - 1):
                md.plot(N.x[i:i+2],N.y[i:i+2],N.z[i:i+2], color='black')
                md.plot(M.x[i:i+2],M.y[i:i+2],M.z[i:i+2], color='blue')
        plt.show()