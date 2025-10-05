def p(g):
 W=len(g[0]);r1,c1=min(y:=[divmod(i,W)for i,v in enumerate(sum(g,[]))if v==4]);r2,c2=max(y);b=r2+1-r1;a=c2+1-c1;mr,mc,*_=min(t:=[(r,c,g[r][c])for r in range(len(g))for c in range(W)if r>r2 and g[r][c]>0]);i=[(r-r1,c-c1,g[r][c])for r in range(r1,r2+1)for c in range(c1,c2+1)if g[r][c]>0!=g[r][c]-4]
 for M in range(1,5):
  I,J,V=min(i)
  for R,C,w in t:
   if w==V:
    d,e=I-(R-mr)*M,J-(C-mc)*M;o=[[0]*a for _ in range(b)];[(r:=(R-mr)*M+d+k//M,c:=(C-mc)*M+e+k%M,b>r>=0<=c<a and o[r].__setitem__(c,v))for R,C,v in t for k in range(M*M)]
    if all(o[r][c]==g[r1+r][c1+c]for r,c,_ in i):o[0][0]=o[0][-1]=o[-1][0]=o[-1][-1]=4;return o
