def p(g):
 a=[any(r) for r in g]+[0]
 c=[]
 for b in range(len(g),0,-1):
  if not a[b] and a[b-1]:
   c+=[b-1]
 for d in c:
  i=0
  while g[d][i]==0:
   i+=1
  g[d][i-1]=g[d][i]
  i=len(g[0])-1
  while g[d][i]==0:
   i-=1
  g[d-1][i]=0
  g[d-1][i-1]=g[d][i]
  g[d][i]=0
 return [[0]+r[:-1]for r in g]
