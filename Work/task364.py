def p(g,R=range,L=len):
 o=[r[:]for r in g];H,W=L(g),L(g[0]);V=set()
 for y in R(H):
  for x in R(W):
   if g[y][x]==3 and(y,x)not in V:
    q=[(y,x)];S=set()
    while q:
     i,j=q.pop()
     if(i,j)in V or g[i][j]-3:continue
     V.add((i,j));S.add((i,j))
     i and q.append((i-1,j));i+1<H and q.append((i+1,j));j and q.append((i,j-1));j+1<W and q.append((i,j+1))
    a=min(y for y,x in S);b=max(y for y,x in S);c=min(x for y,x in S);d=max(x for y,x in S)
    T=sum((a,x)in S for x in R(c,d+1));B=sum((b,x)in S for x in R(c,d+1))
    Lb=sum((y,c)in S for y in R(a,b+1));Rb=sum((y,d)in S for y in R(a,b+1))
    h=any(((i>0 and(i-1,j)in S)+(i+1<H and(i+1,j)in S)+(j>0 and(i,j-1)in S)+(j+1<W and(i,j+1)in S))==3 for i,j in S)
    k=2 if h else 6 if(Lb>1 and Rb>1 and(T>1)^(B>1))or(T>1 and B>1 and(Lb>1 or Rb>1))else 1
    for i,j in S:o[i][j]=k
 return o