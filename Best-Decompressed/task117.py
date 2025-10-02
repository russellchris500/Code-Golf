p=lambda g,R=range,l=len:(
 t:=next((i,j)for i in R(1,l(g)-1)for j in R(1,l(g)-1)if(v:=g[i][j])and g[i-1][j-1]==v==g[i-1][j+1]==g[i+1][j-1]==g[i+1][j+1]and(i<2 or j<2 or g[i-2][j-2]-v)),
 y:=t[0],x:=t[1],n:=l(g),
 q:=next((r,c)for r in R(n)for c in R(n)if g[r][c]and abs(r-y)+abs(c-x)>2),
 [(v:=g[r][c])and(g[2*y-r].__setitem__(c,v),g[r].__setitem__(2*x-c,v),g[2*y-r].__setitem__(2*x-c,v))
  for r in(R(y)if q[0]<y else R(y+1,n))for c in(R(x)if q[1]<x else R(x+1,n))if g[r][c]],
 g)[-1]
