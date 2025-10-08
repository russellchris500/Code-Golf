def p(i):
 g=[r[:]for r in i];c=0
 for r in range(9):
  for j in[1,3,5,7]:
   if g[r][j]==5:
    c+=1
    for k in range(r,9):g[k][j]=c
 return g
