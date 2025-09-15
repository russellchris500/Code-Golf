def p(g):
 h=len(g);w=len(g[0]);m=[r[:]for r in g];s=set()
 def f(x,y):
  if(x,y)in s or x<0 or y<0 or x>=w or y>=h:return x<0 or y<0 or x>=w or y>=h
  if g[y][x]:return 0
  s.add((x,y));return f(x+1,y)|f(x-1,y)|f(x,y+1)|f(x,y-1)
 for y in range(h):
  for x in range(w):
   if g[y][x]==0 and(x,y)not in s:
    t=set();s.clear()
    if not f(x,y):
     for i,j in s:m[j][i]=4
 return m