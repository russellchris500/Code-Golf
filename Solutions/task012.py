def p(g):
 o=[r[:]for r in g];a=range(2,10)
 for y in a:
  for x in a:
   if g[y][x]*g[y-1][x]*g[y+1][x]:o[y-2][x-2]=o[y-2][x+2]=o[y+2][x-2]=o[y+2][x+2]=g[y][x];o[y-2][x]=g[y-1][x];o[y+2][x]=g[y+1][x];o[y][x-2]=g[y][x-1];o[y][x+2]=g[y][x+1]
 return o