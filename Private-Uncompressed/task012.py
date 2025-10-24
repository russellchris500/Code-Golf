def p(g):
 for y in range(2,10):
  for x in range(2,10):
   if g[y][x]*g[y-1][x]*g[y+1][x]*g[y][x-1]*g[y][x+1]:
    for d in[1,2]:g[y-d][x-d]=g[y-d][x+d]=g[y+d][x-d]=g[y+d][x+d]=g[y][x];g[y-2][x]=g[y+2][x]=g[y][x-2]=g[y][x+2]=g[y-1][x]
 return g
