def p(g):
 for y,r in enumerate(g):
  if I:=[j for j,v in enumerate(r)if 0<v!=8]:s,k=I[0],len(I);break
 o=[r[s-1:s+k+1]for r in g[y:y+k+2]]
 a=next(i for i,u in enumerate(g)if 8 in u);b=min(u.index(8)for u in g if 8 in u)
 for y in range(k):
  for x in range(k):
   if g[a+y][b+x]==8:
    d=[y,k+~y,x,k+~x];m=min(d);o[y+1][x+1]=8 if d.count(m)>1else[o[0][1],o[-1][1],o[1][0],o[1][-1]][d.index(m)]
 return o
