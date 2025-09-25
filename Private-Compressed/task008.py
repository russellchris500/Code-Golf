def p(g):
 def f(h):
  s=o=-1
  for r in range(len(h)-1):
   if 8 in h[r]and 8 in h[r+1]:s=r;break
  for r in range(len(h)):
   if 2 in h[r]:o=r;break
  if s>o>-1:
   e=sum(1 for r in h[o+1:s]if 0==max(r))
   return[[0]*len(h[0])]*e+[r for i,r in enumerate(h)if i<=o or i>=s or max(r)]
  return h
 for _ in 0,1:
  for _ in 0,1:g=f(g);g=g[::-1]
  g=[*map(list,zip(*g))]
 return g