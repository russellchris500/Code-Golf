def p(g):
 g=[[2 if c==1 else c for c in r]for r in g]
 for n in range(2,6):
  if all(g[j]==g[j%n]for j in range(len(g))):return g+[g[j%n]for j in range(len(g),len(g)+3)]