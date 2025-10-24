def p(g,R=range):
 h,w=len(g),len(g[0]);P=b=0
 for i in R(h-2):
  for j in R(w-2):c=sum(g[r][c]not in[0,5]for r in R(i,i+3)for c in R(j,j+3));c>b and(P:=[[g[r][c]for c in R(j,j+3)]for r in R(i,i+3)],b:=c)
 for i in R(h):
  for j in R(w):
   if g[i][j]==5:[P*(0<=n<h)*(0<=m<w)and g[n].__setitem__(m,P[d+1][e+1])for d in R(-1,2)for e in R(-1,2)for n,m in[(i+d,j+e)]];break
 return g
