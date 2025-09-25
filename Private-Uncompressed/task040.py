q=lambda g:[[[j,c[0],c[-1]][(j==3)*(1+i//5)]for i,j in enumerate(c)]for c in g]
p=lambda g:[*zip(*q([*zip(*g)]))]if all(g[0])else q(g)