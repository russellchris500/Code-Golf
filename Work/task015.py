def p(g):
 o=[r*1 for r in g];e=enumerate
 for y,r in e(g):
  for x,v in e(r):
   for d in 1,-1:
    if v==2:o[y+d][x+d]=o[y+d][x-d]=4
    if v==1:o[y+d][x]=o[y][x+d]=7
 return o