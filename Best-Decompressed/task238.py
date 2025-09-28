def p(g,R=range,L=len,M=min,E=enumerate):
  for y,row in E(g):
    if I:=[j for j,v in E(row) if 0<v!=8]: s=I[0];k=L(I);break
  o=[r[s-1:s+k+1]for r in g[y:y+k+2]]
  T=[o[0][1],o[-1][1],o[1][0],o[1][-1]]
  a=next(i for i,u in E(g)if 8 in u);b=min(u.index(8)for u in g if 8 in u)
  for y in R(k):
    for x in R(k):
      d=y,k-1-y,x,k-1-x;q=M(d)
      o[y+1][x+1]=(8 if d.count(q)>1 else T[d.index(q)])*(g[a+y][b+x]//8)
  return o
