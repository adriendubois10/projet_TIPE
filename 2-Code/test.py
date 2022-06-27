import matplotlib.pyplot as plt

X = [10*i for i in range(-1,11)]
Y = [-1]+[10]*11

fig, ax = plt.subplots()
ax.xaxis.set_ticks(X)
plt.scatter(X,Y)
plt.show()