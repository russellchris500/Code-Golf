def p(g):
 f,n=[],[]
 for i in range(len(g)):
  for j in range(len(g[0])):
   if g[i][j]==4:f.append((i,j))
   elif g[i][j]>0:n.append((i,j,g[i][j]))
 f.sort()
 t,l=f[0];b,r=f[-1]
 o=[[g[i][j]for j in range(l,r+1)]for i in range(t,b+1)]

 # Extract pattern bounding box
 pn=[p for p in n if not(t<=p[0]<=b and l<=p[1]<=r)]
 if pn:
  pt,pl=min(p[0]for p in pn),min(p[1]for p in pn)
  pb,pr=max(p[0]for p in pn),max(p[1]for p in pn)

  # Check if pattern should be flipped horizontally
  flip=False
  for pi in range(pt,pb+1):
   if g[pi][pl]>0 and g[pi][pl]!=4 and pi-pt+1<len(o)-1:
    if g[pi][pl]!=o[pi-pt+1][0]:flip=True

  # Place pattern (flipped or normal)
  for pi in range(pt,pb+1):
   for pj in range(pl,pr+1):
    if g[pi][pj]>0 and g[pi][pj]!=4:
     if flip:oi,oj=pi-pt+1,len(o[0])-1-(pj-pl+1)
     else:oi,oj=pi-pt+1,pj-pl+1
     if 0<=oi<len(o)-1 and 0<=oj<len(o[0])-1:o[oi][oj]=g[pi][pj]
 return o