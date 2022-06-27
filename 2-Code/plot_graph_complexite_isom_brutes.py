import matplotlib.pyplot as plt
from geometrie_et_aux import fact
from numpy import log10

def brute(n,q):
    return sum([log10(x) for x in range(1,n*q)])

def brute_tri(n,q):
    return n * sum([log10(x) for x in range(1,q)])

QC = [(2,'b'),(3,'g'),(5,'r'),(7,'purple')]
N = [n for n in range(1,51)]

fig, ax = plt.subplots()
for (q,c) in QC:
    B = [brute(n,q) for n in N]
    BT = [brute_tri(n,q) for n in N]
    plt.plot([0]+N, [0]+B, color =c, label = 'brute avec q = {} '.format(q))
    plt.plot([0]+N, [0]+BT, color = c, ls = '--', label = '  tri    avec q = {} '.format(q))
plt.ylim(0,300)
plt.xlabel("n, taille de G et H", loc = 'right')
plt.ylabel(" C(n) ", loc = 'top')
plt.title(" Complexité par force brute (nq éléments) et par tri des sommets (n paquets de taille q)")

ticks = ax.get_yticklabels()
print(ticks)
posticks =ax.get_yticks()
for i in range(len(posticks)):
    ticks[i].set_text('$10^{'+str(int(posticks[i]))+'}$')
    ticks[i].set_usetex(True)
ax.set_yticks(posticks)
ax.set_yticklabels(ticks)
plt.legend()
plt.show()
    