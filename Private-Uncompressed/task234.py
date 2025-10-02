def p(g):
 b=all(len({*r})<3for r in g);g=(1-b)*[*zip(*g)]+b*g;l=0
 for i,r in enumerate(g):
  if sum(map(bool,r))==1:
   if l==0:s=i;c=max(r)
   l+=1
  if max(r)>0:d=max(r)
 g=g[:s]+g[s+l:];w=len(g[0]);g=[[0]*w]*(d!=c)*l+g+[[0]*w]*(d==c)*l;g=(1-b)*[*zip(*g)]+b*g;return g