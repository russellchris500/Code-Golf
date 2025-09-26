a=lambda g:(sum(z:=[3 in r for r in g])>1,z.index(1),[3 in r for r in zip(*g)].index(1))
def p(g):
 b,r,c=a(g)
 if b:g=[*zip(*g)];r,c=c,r
 def e(h,i,j,c,l,f):
  d=[[*r] for r in h]
  if d[i][j+f]in{c,8}:return
  while 0<=j<len(d) and d[i][j]not in{c,8}:d[i][j]=3;j+=f
  if 0<=j<len(d) and d[i][j]==c:w([*zip(*d)],j-f,i,l+1)
 def w(h,x,y,l):
  nonlocal g
  if l<3:e(h,x,y,[8,2][l>1],l,1);e(h,x,y,[8,2][l>1],l,-1)
  else:g=h
 w(g,r,c,0)
 if not b:g=[*zip(*g)]
 return g