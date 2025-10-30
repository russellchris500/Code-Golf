def p(g):
 c=set();t=[]
 for a in range(100):
  n,a=a//10,a%10
  if(n,a)in c:continue
  r=g[n][a];p=[(n,a)];u={(n,a)};c|={p[0]}
  for f,x in p:
   for a in[(f+d,x+e)for d,e in[(-1,0),(1,0),(0,-1),(0,1)]]:
    if-1<a[0]<10>a[1]>-1and a not in c and g[a[0]][a[1]]==r:c|={a};p+=[a];u|={a}
  t+=[(r,u)]
 r=[a for c,a in t if c==5];p=[];j=[]
 for c,a in t:
  if c<1:
   f=lambda s,p:[min,max][p>1](c[p%2]for c in s)
   if any(all(f(a,c)>=f(n,c)if c<2else f(a,c)<=f(n,c)for c in range(4))for n in r):p+=[a]
  elif c>0!=5:j+=[(c,a)]
 r=lambda s:frozenset((a-(c:=min(s))[0],n-c[1])for a,n in s);a={};l={}
 for f in p:s=r(f);a[s]=a.get(s,[])+[f]
 for c,f in j:s=r(f);l[s]=l.get(s,[])+[(c,f)]
 u={c:sum(1for a,n in j if a==c)for c,a in j}
 for s,h in a.items():
  m=l[s]
  if len(m)>1and u:m=[x for x in m if x[0]!=max(u,key=u.get)]or m
  for z,(c,f)in zip(h,m):
   for n,a in f:g[n][a]=0
   for n,a in z:g[n][a]=c
 return g
