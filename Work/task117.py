def p(g):
 n,o,c=len(g),[r[:]for r in g],{}
 for r in range(n):
  for x in range(n):
   if g[r][x]:c[g[r][x]]=c.get(g[r][x],[])+[(r,x)]
 for a in c:
  for b in c:
   if a!=b:
    ar,ac=sum(r for r,x in c[a])/len(c[a]),sum(x for r,x in c[a])/len(c[a])
    for r,x in c[b]:
     nr,nx=int(2*ar-r),int(2*ac-x)
     if 0<=nr<n and 0<=nx<n:o[nr][nx]=g[r][x]
 return o