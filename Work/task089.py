def p(p,f=range):
 l,o=len(p),len(p[0]);s=[h[:]for h in p];k=[[0]*o for h in f(l)];d=[]
 for i in f(l):
  for q in f(o):
   if k[i][q]or p[i][q]<1:continue
   r=[(i,q)];a=[]
   while r:
    h,n=r.pop()
    if h<0 or h>=l or n<0 or n>=o or k[h][n]or p[h][n]<1:continue
    k[h][n]=1;a+=[(h,n,p[h][n])];r+=[(h+x,n+y)for x,y in[(-1,0),(1,0),(0,-1),(0,1),(1,1),(1,-1),(-1,1),(-1,-1)]if-1<h+x<l>n+y>-1<o and k[h+x][n+y]<1and p[h+x][n+y]>0]
   a and d.append(a)
 g,e,c,p=[],[],[],[]
 for a in d:
  v={n for h,h,n in a}
  if len(a)<2:
   r,h,n=a[0]
   if n==2:c+=[(r,h)]
   elif n>2:p+=[(r,h)]
  else:
   if 2in v:g+=[a]
   if 3in v:e+=[a]
 def a(u,z,t,f=0):
  n=next(((h,n)for h,n,a in u if a==z),None)
  if not n:return
  i,q=n
  for r,n in t:
   for d,g,e in u:
    c,h=d-i,g-q
    if f:h=-h
    x,y=r+c,n+h
    if-1<x<l>y>-1<o:s[x][y]=e
 for n in g:a(n,2,c,1)
 for n in e:a(n,3,p)
 return s
