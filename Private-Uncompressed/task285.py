def p(G,R=range,L=len):
 H,W=L(G),L(G[0]);V=set();Z=[]
 for y in R(H):
  for x in R(W):
   if G[y][x]and(y,x)not in V:
    k=G[y][x];S=[(y,x)];V.add((y,x));h=[]
    while S:
     a,b=S.pop();h.append((a,b))
     for dy,dx in((1,0),(-1,0),(0,1),(0,-1)):
      u,v=a+dy,b+dx
      if 0<=u<H and 0<=v<W and G[u][v]==k and(u,v)not in V:V.add((u,v));S.append((u,v))
    Z.append(h)
 def inv(t,Y,X,py,px):
  if t==0:return py-Y,px-X
  if t==1:return py-Y,X-px-1
  if t==2:return Y-py-1,px-X
  return Y-py-1,X-px-1
 def fwd(t,r,c,py,px):
  if t==0:return py-r,px-c
  if t==1:return py-r,px+c+1
  if t==2:return py+r+1,px-c
  return py+r+1,px+c+1
 I=[]
 for P in Z:
  S=set(P);ok=()
  for py,px in P:
   for t in R(4):
    Rw=[];Cl=[];S0=[];bad=0
    for Y,X in P:
     r,c=inv(t,Y,X,py,px)
     if r<0 or c<0:bad=1;break
     Rw.append(r);Cl.append(c);S0.append((r,c))
    if bad:continue
    n=max(Rw)+1
    if n!=max(Cl)+1:continue
    if {(fwd(t,r,c,py,px))for r,c in S0}==S:ok=(py,px,t,n,set(S0));break
   if ok:break
  if not ok:
   rs=[a for a,_ in P];cs=[b for _,b in P]
   py,px=min(rs),min(cs);t=0;S0={(Y-py,X-px)for Y,X in P};n=max(max(r for r,_ in S0),max(c for _,c in S0))+1
   ok=(py,px,t,n,S0)
  I.append(ok)
 C=[0,0,0,0];S=[0,0,0,0]
 for (py,px,t,n,S0),P in zip(I,Z):
  if not S[t]:C[t]=G[P[0][0]][P[0][1]];S[t]=1
 O=[r[:] for r in G]
 for py,px,_,n,S0 in I:
  for a in R(4):
   k=C[a]
   if not k:continue
   for r,c in S0:
    if a==0:Y,X=py-r,px-c
    if a==1:Y,X=py-r,px+c+1
    if a==2:Y,X=py+r+1,px-c
    if a==3:Y,X=py+r+1,px+c+1
    if 0<=Y<H and 0<=X<W:O[Y][X]=k
 return O
