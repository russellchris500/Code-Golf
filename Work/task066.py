# a=lambda g:(sum(z:=[3 in r for r in g])>1,z.index(1),[3 in r for r in zip(*g)].index(1)) # returns b,r,c-b is 1 if needs flipping, r and c are location of a green pixel
# def p(g):
#  b,r,c=a(g)
#  if b:g=[*zip(*g)];r,c=c,r
#  def e(h,i,j,c,l,f):
#   d=[[*r] for r in h]
#   if d[i][j+f]in{c,8}:return
#   while 0<=j<len(d) and d[i][j]not in{c,8}:d[i][j]=3;j+=f;print(f"j={j}")
#   if 0<=j<len(d) and d[i][j]==c:w([*zip(*d)],j-f,i,l+1)
#  def w(h,x,y,l):
#   nonlocal g
#   if l<3:e(h,x,y,[8,2][l>1],l,1);e(h,x,y,[8,2][l>1],l,-1)
#   else:g=h
#  w(g,r,c,0)
#  if not b:g=[*zip(*g)]
#  return g
def p(g):
 z=[3in r for r in g];b,r,c=sum(z)>1,z.index(1),[3in r for r in zip(*g)].index(1)
 if b:g=[*zip(*g)];r,c=c,r
 def e(h,i,j,c,l,f):
  d=[[*r]for r in h]
  if d[i][j+f]in{c,8}:return
  while-1<j<len(d)and d[i][j]not in{c,8}:d[i][j]=3;j+=f
  -1<j<len(d)and d[i][j]==c and w([*zip(*d)],j-f,i,l+1)
 def w(h,x,y,l):
  nonlocal g
  l<3and(e(h,x,y,[8,2][l>1],l,1),e(h,x,y,[8,2][l>1],l,-1))or(g:=h)
 w(g,r,c,0)
 return[*zip(*g)]if~-b else g