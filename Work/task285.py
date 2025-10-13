from collections import*
def p(i):
 o=[r[:]for r in i];H,W=len(i),len(i[0])
 for R in range(H-1):
  for C in range(W-1):
   q=[i[R][C],i[R][C+1],i[R+1][C],i[R+1][C+1]]
   if len(set(q))==4:
    d=Counter(q);v={(R,C),(R,C+1),(R+1,C),(R+1,C+1)};L=deque(v)
    while L:
     x,y=L.popleft()
     for a,b in(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1):X,Y=x+a,y+b;0<=X<H and 0<=Y<W and(X,Y)not in v and i[X][Y]and[v.add((X,Y)),d.update([i[X][Y]]),L.append((X,Y))]
    D=[c for c,_ in d.most_common()if c][0];r,c=R+.5,C+.5;p=q.index(D)
    for x,y in[(x,y)for x,y in v if i[x][y]==D]:
     for X,Y,P in(int(2*r-x),y,p^2),(x,int(2*c-y),p^1),(int(2*r-x),int(2*c-y),p^3):
      if-1<X<H>Y>-1<W:o[X][Y]=q[P]
 return o