def p(g):
 h=[x[:] for x in g]
 for r in range(1,len(g)-1):
  for c in range(1,len(g[0])-1):
   if g[r][c-1]*g[r][c+1]*g[r-1][c]*g[r+1][c]>0:h[r][c]=0
 return h
