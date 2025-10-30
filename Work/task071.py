def p(n):
 from collections import defaultdict as a
 d,f=len(n),len(n[0]);l=a(list)
 for a in range(d):
  for c in range(f):
   if n[a][c]:l[n[a][c]].append((a,c))
 o,t=l.keys();o,t=(o,t)if len(l[o])<len(l[t])else(t,o);a,e=l[t],set(l[t]);x=set(l[o]);x=max(range(2*f-1),key=lambda o:sum(1for(a,c)in a if 0<=(k:=o-c)<f and((a,k)in e or(a,k)in x)));n=[[0]*f for _ in range(d)]
 for(a,c)in a:n[a][c]=t
 for(a,c)in l[o]:
  if 0<=(m:=x-c)<f and(a,m)in e:n[a][c]=t
 return n