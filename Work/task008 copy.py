def p(g):
 s=o=-1
 for r in range(len(g)-1):
  if 8 in g[r]and 8 in g[r+1]:s=r;break
 for r in range(len(g)):
  if 2 in g[r]:o=r;break
 if s>o>-1:
  e=sum(1 for r in g[o+1:s]if 0==max(r))
  return[[0]*len(g[0])]*e+[r for i,r in enumerate(g)if i<=o or i>=s or max(r)]
 return g