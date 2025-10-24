def p(i):
 for R in range(len(i)-1):
  for C in range(len(i[0])-1):
   q=[i[R][C],i[R][C+1],i[R+1][C],i[R+1][C+1]]
   if len({*q})==4:
    v={(R,C),(R,C+1),(R+1,C),(R+1,C+1)};L=[*v]
    while L:
     x,y=L.pop()
     for a,b in(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1):
      X,Y=x+a,y+b
      0<=X<len(i)and 0<=Y<len(i[0])and(X,Y)not in v and i[X][Y]and(v.add((X,Y)),L.append((X,Y)))
    D=max(q,key=lambda c:sum(i[x][y]==c for x,y in v));p=q.index(D)
    for x,y in v:
     if i[x][y]==D:
      for X,Y,P in(2*R+1-x,y,p^2),(x,2*C+1-y,p^1),(2*R+1-x,2*C+1-y,p^3):
       if-1<X<len(i)>Y>-1<len(i[0]):i[X][Y]=q[P]
 return i
