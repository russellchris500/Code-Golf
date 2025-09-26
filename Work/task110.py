def p(g):
 for _ in range(99):
  for i in range(29):
   for j in range(29):
    if g[i][j]<1:n=[g[i+x][j+y]for x in(-1,0,1)for y in(-1,0,1)if 0<=i+x<29 and 0<=j+y<29 and g[i+x][j+y]];g[i][j]=n[0]if n else 0
 return g