def p(g):
 o=[r[:]for r in g]
 for y in range(2,10):
  for x in range(2,10):
   if g[y][x]*g[y-1][x]*g[y+1][x]*g[y][x-1]*g[y][x+1]:
    o[y-2][x-2]=o[y-2][x+2]=o[y+2][x-2]=o[y+2][x+2]=g[y][x]
    o[y-2][x]=g[y-1][x];o[y+2][x]=g[y+1][x];o[y][x-2]=g[y][x-1];o[y][x+2]=g[y][x+1]
 return o