def p(g,R=range,L=len):
 h,w=L(g),L(g[0])
 def f(i,j):
  g[i][j]=0;S.add((i,j))
  i and g[i-1][j]==3 and f(i-1,j)
  i+1<h and g[i+1][j]==3 and f(i+1,j)
  j and g[i][j-1]==3 and f(i,j-1)
  j+1<w and g[i][j+1]==3 and f(i,j+1)
 for y in R(h):
  for x in R(w):
   if g[y][x]-3:continue
   S=set();f(y,x);c=b=0
   for i,j in S:
    u=(i-1,j)in S;d=(i+1,j)in S;l=(i,j-1)in S;r=(i,j+1)in S;t=u+d+l+r
    c|=t>2;b+=t==2 and(u^d)and(l^r)
   k=(1,6)[b>1];k=2 if c else k
   for i,j in S:g[i][j]=k
 return g
