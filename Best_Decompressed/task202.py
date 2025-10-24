def p(l,g=range):
 t=None;A,n=len(l),len(l[0]);D=[(lambda s:next(iter(s))if len(s)<=1else t)({x for x in B if x})for B in l];N=[(lambda s:next(iter(s))if len(s)<=1else t)({l[x][B]for x in g(A)if l[x][B]})for B in g(n)]
 def s(v):
  B=[];C=0
  for t in g(1,len(v)+1):
   if t==len(v)or v[t]!=v[t-1]:B.append((C,t-1));C=t
  return B
 if all(B is not t for B in D)and len(set(D))>1:
  for(I,J)in s(D):
   for B in g(n):
    if any(l[r][B]==0for r in g(I,J+1)):
     for C in g(I,J+1):l[C][B]=0
  return l
 if all(B is not t for B in N)and len(set(N))>1:
  for(E,L)in s(N):
   for C in g(A):
    if any(l[C][r]==0for r in g(E,L+1)):
     for B in g(E,L+1):l[C][B]=0
 return l

