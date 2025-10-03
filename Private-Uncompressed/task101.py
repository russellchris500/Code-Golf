def p(u):
 k,o,*t=0,1
 def h(u):
  if u in e:r[u]=e.pop(u);h((u[0]-1,u[1]));h((u[0]+1,u[1]));h((u[0],u[1]-1));h((u[0],u[1]+1))
 while o:
  e,o={(p,m):v for p,u in enumerate(u)for m,v in enumerate(u)if v},[]
  while e:o+=[r:={}];h(min(e))
  if t:o=[u for u in o if{1}-{*u.values()}];k=0
  if o:U=o[k];p,m=min(O:=[u for u in U if U[u]>1])
  if not t:t=[(u[0]-p,u[1]-m)for u in U if U[u]==1];k+=1
  elif o:
   i=min(len(O)+6,15)//5
   for r,v in t:
    for e in range(i*i):u[p+r*i+e//i][max(0,m+v*i+e%i)]=1
 return u