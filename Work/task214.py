def p(g):
 o=[r[:]for r in g]
 for i in range(3):
  for j in range(3):
   o[i][4+j]=g[2-j][i]
   o[i][8+j]=g[2-i][2-j]
 return o