def p(g):
 o=[r[:]for r in g]
 for y in range(2,10):
  for x in range(2,10):
   if g[y][x]*g[y-1][x]*g[y+1][x]*g[y][x-1]*g[y][x+1]:
    for d in[1,2]:o[y-d][x-d]=o[y-d][x+d]=o[y+d][x-d]=o[y+d][x+d]=g[y][x];o[y-2][x]=o[y+2][x]=o[y][x-2]=o[y][x+2]=g[y-1][x]
 return o
