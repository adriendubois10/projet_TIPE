def isomorphism(G,H):
    if G.nbr != H.nbr:
        return False, []
    sn = permutations(G.nbr) # représente $\Sigma_n$
    for s in sn:
        res = test_isomorphism(G, H, s)
        if res != (False, []):
            return res
    return False, []