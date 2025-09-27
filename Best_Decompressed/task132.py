def p(g):
 r=[list(x)for x in g]
 s=sum(g,[])
 w=len(g[0])
 for v in set(s)-{0}:
  u=s.index(v)
  try:z=s.index(v,u+1)
  except:z=u
  a,b=divmod(u,w)
  c,e=divmod(z,w)
  for i in range(min(a,c),max(a,c)+1):
   for j in range(min(b,e),max(b,e)+1):r[i][j]=v
 return r
