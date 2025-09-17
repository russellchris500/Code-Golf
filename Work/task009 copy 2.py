def q(g):
 r=[x[:]for x in g]
 for i,w in enumerate(r):
  for c in range(1,10):
   p=[j for j,v in enumerate(w)if v==c]
   if len(p)>3:
    for j in range(min(p),max(p)+1):r[i][j]=c
 return r
def p(g):
 n=len(g);z=range(n)
 h=[[g[i][j]for j in z if j%3<2]for i in z if i%3<2]
 a=q(h)
 b=q([[h[j][i]for j in range(len(h))]for i in range(len(h[0]))])
 b=[[b[j][i]for j in range(len(b))]for i in range(len(b[0]))]
 c=[[max(a[i][j],b[i][j])for j in range(len(a[0]))]for i in range(len(a))]
 r,x,y=[[g[i][j]for j in z]for i in z],0,0
 for i in z:
  if i%3<2:
   y=0
   for j in z:
    if j%3<2:r[i][j]=c[x][y];y+=1
   x+=1
 return r