def p(g,i=range):
 f=[]
 for r in g:e=sum([[s]*2for s in r],[]);f+=[e,e]
 h,w=len(f),len(f[0]);a=[[0]*w for _ in i(h)];p=[]
 for r in i(h):
  for s in i(w):
   if f[r][s]!=2or a[r][s]:continue
   d=[(r,s)];a[r][s]=1;k=[]
   while d:
    o,b=d.pop();k+=[(o,b)]
    for j in-1,0,1:
     for g in-1,0,1:
      if j==g==0:continue
      c,z=o+j,b+g
      if 0<=c<h and 0<=z<w and not a[c][z]and f[c][z]==2:a[c][z]=1;d+=[(c,z)]
   p+=k,
 n=[(s,r)for s in i(h)for r in i(w)if f[s][r]==2]
 def g(p,m,n,h):
  for s in i(p,n+1):
   for r in i(m,h+1):f[s][r]=4
 def b(o):y,x=zip(*o);g(min(y),min(x),max(y),max(x))
 for o in p:b(o)
 def a(s,f):return min(abs(o-z)+abs(c-k)for(o,c)in s for(z,k)in f)
 e=len(p)
 for r in i(e):
  for s in i(e):
   if a(p[r],p[s])<5:b(p[r]+p[s])
 for(r,s)in n:f[r][s]=2
 return[s[::2]for s in f[::2]]
