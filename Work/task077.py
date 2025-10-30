def p(g):
 r=[(i,j)for i,R in enumerate(g)for j,v in enumerate(R)if v==2];P={c:c for c in r}
 def f(x):P[x]=P[x]if P[x]==x else f(P[x]);return P[x]
 for i,c in enumerate(r):
  for d in r[i+1:]:max(abs(c[0]-d[0]),abs(c[1]-d[1]))<3>(P.__setitem__(f(c),f(d))or 9)
 I={}
 for c in r:k=f(c);I[k]=I.get(k,[])+[c]
 o=[R[:]for R in g]
 for C in I.values():y,x=zip(*C);[o[i].__setitem__(j,4)for i in range(min(y),max(y)+1)for j in range(min(x),max(x)+1)if o[i][j]-2]
 return o