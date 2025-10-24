def p(l,R=range):
 t,o=len(l),len(l[0]);h=[list(w)for w in l];M=min;X=max
 for r in R(t):
  for c in R(o):
   if l[r][c]:continue
   for H in R(1,t-r+1):
    for W in R(1,o-c+1):
     if not all(l[r+d][c+e]==0 for d in R(H)for e in R(W)):continue
     s=-1 if c else 0;T=W+(c+W<o);p=set()
     if r:p|={(r-1,c+e)for e in R(s,T)}
     if r+H<t:p|={(r+H,c+e)for e in R(s,T)}
     if c:p|={(r+d,c-1)for d in R(H)}
     if c+W<o:p|={(r+d,c+W)for d in R(H)}
     if not p or any(l[y][x]-5 for y,x in p):continue
     P=list(p);a,b,d,e=M(y for y,x in P),X(y for y,x in P),M(x for y,x in P),X(x for y,x in P);N={(Y,E)for y,x in[(a,d),(a,e),(b,d),(b,e)]for f,g in[(0,1),(0,-1),(1,0),(-1,0)]for Y in[y+f]for E in[x+g]if 0<=Y<t and 0<=E<o}
     if{(y,x)for y in R(t)for x in R(o)if l[y][x]==5}.isdisjoint(N-p):
      for d in R(H):
       for e in R(W):h[r+d][c+e]=4
 return h
