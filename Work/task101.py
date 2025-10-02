# def p(g):
#  h,w=len(g),len(g[0])
#  b=[(i,j)for i in range(h)for j in range(w)if g[i][j]==1]
#  r=[(i,j)for i in range(h)for j in range(w)if g[i][j]==2]
#  tr=[p for p in r if any(abs(p[0]-q[0])+abs(p[1]-q[1])==1 for q in b)]
#  ir=[p for p in r if p not in tr]
#  if not(tr and ir and b):return g
#  def bb(l):return min(p[0]for p in l),max(p[0]for p in l),min(p[1]for p in l),max(p[1]for p in l)
#  tri,trx,trj,try_=bb(tr)
#  iri,irx,irj,iry=bb(ir)
#  bri,brx,brj,bry=bb(b)
#  tci,tcj=(tri+trx)//2,(trj+try_)//2
#  ici,icj=(iri+irx)//2,(irj+iry)//2
#  bci,bcj=(bri+brx)//2,(brj+bry)//2
#  tw,th=try_-trj+1,trx-tri+1
#  iw,ih=iry-irj+1,irx-iri+1
#  s=min(iw//tw,ih//th)if tw and th else 1
#  for bi,bj in b:
#   di,dj=bi-bci,bj-bcj
#   ni,nj=ici+di*s,icj+dj*s
#   if 0<=ni<h and 0<=nj<w and g[ni][nj]!=2:g[ni][nj]=1
#  return g
def p(u):
 print("") #
 k,o,*t=0,1
 def p(u):
  if u in e:r[u]=e.pop(u);p((u[0]-1,u[1]));p((u[0]+1,u[1]));p((u[0],u[1]-1));p((u[0],u[1]+1))
 while o:
  #Find objects. o is list of dicts with key=(x,y) and value=color
  e,*o={(p,m):v for p,u in enumerate(u)for m,v in enumerate(u)if v}
  while e:o+=[r:={}];p(min(e))
  # Remove completed templates if template found
  if t:o=[u for u in o if {1}-{*u.values()}];k=0
  # Get the min coordinates for red, U is current object
  U=o[k];p,m=min(O:=[u for u in U if U[u]>1])
  if ~-t:
   #Search for the template t. It contains blue. Offset it by min if found.
   t=[(u[0]-p,u[1]-m)for u in U if 1 in U.values()]
  else:
   #Get the size of the first red square
   i=min([*U.values()].count(2)+6,15)//5
   #Match with first red square
   for r,v in t[0]:
    for e in range(i*i):u[]
  return u