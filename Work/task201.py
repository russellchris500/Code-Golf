def p(g):
 f,n=[],[]
 for i in range(len(g)):
  for j in range(len(g[0])):
   if g[i][j]==4:f.append((i,j))
   elif g[i][j]>0:n.append((i,j,g[i][j]))
 f.sort()
 t,l=f[0];b,r=f[-1]
 o=[[g[i][j]for j in range(l,r+1)]for i in range(t,b+1)]
 for i,j,v in n:
  if not(t<=i<=b and l<=j<=r):
   if v==2:oi,oj=i-t+1,j-l
   else:oi,oj=i-t+1,r+l-j
   if 0<=oi<len(o)-1 and 0<=oj<len(o[0]):o[oi][oj]=v
 return o