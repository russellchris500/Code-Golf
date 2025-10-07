def p(g,R=range,L=len):
 h,w=L(g),L(g[0]);T=()
 for I in R(h-6):
  for J in R(w-6):
   if g[I][J]==g[I][J+6]==g[I+6][J]==g[I+6][J+6]==5:
    Q=[(y-1,x-1)for y in R(1,6)for x in R(1,6)if(v:=g[I+y][J+x])and v-5]
    if Q:
     k=g[I+Q[0][0]+1][J+Q[0][1]+1]
     r,c=zip(*Q);T={(a-min(r),b-min(c))for a,b in Q}
     break
 P={(i,j):v for i in R(h) for j in R(w) if (v:=g[i][j])and v-5}
 while P:
  (y,x),t=P.popitem();S=[(y,x)];q=[(y,x)]
  while q:
   y,x=q.pop()
   for a,b in((1,0),(-1,0),(0,1),(0,-1)):
    n=(y+a,x+b)
    if P.get(n)==t:P.pop(n);S.append(n);q.append(n)
  r,c=zip(*S)
  if {(a-min(r),b-min(c))for a,b in S}==T:
   for y,x in S:g[y][x]=k
 return g