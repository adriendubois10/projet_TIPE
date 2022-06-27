def test_isomorphism(G, H, s):
    for i in range(G.nbr):
        if not [s[j] for j in G.connect[s[i]]]==H.connect[i]:
            break #un terme de la liste d'adjacence diffère
        if i==(G.nbr-1):
            return True, s
    return False, []