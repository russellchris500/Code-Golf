def p(g):
 r=range
 s=r(21)
 for n in r(2,12):
  t=[[0]*n for _ in r(n)]
  ok=1
  for i in s:
   for j in s:
    if g[i][j]>0:
     x,y=i%n,j%n
     if t[x][y]<1:t[x][y]=g[i][j]
     elif t[x][y]!=g[i][j]:ok=0;break
   if not ok:break
  if ok and sum(1 for i in r(n)for j in r(n)if t[i][j]>0)==n*n:
   [g[i].__setitem__(j,t[i%n][j%n])for i in s for j in s if g[i][j]<1]
   break
 return g