def p(i):
 g=[r[:]for r in i]
 H,W=len(i),len(i[0])
 for r,w in enumerate(i):
  for c,v in enumerate(w):
   if v<1:
    l=w[c-1]if c>0 else 0
    rt=w[c+1]if c<W-1 else 0
    if l and rt and l!=rt:
     u=i[r-1][c]if r>0 else 0
     d=i[r+1][c]if r<H-1 else 0
     f=w[c-2]if c>1 else 0
     x=w[c+2]if c<W-2 else 0
     s=sum(z==l for z in[u,d,f,x]if z)-sum(z==rt for z in[u,d,f,x]if z)
     if s>0:b=l
     elif s<0:b=rt
     else:
      lh,rh=w.count(l),w.count(rt)
      b=rt if abs(lh-rh)>2 and rh<lh else l
    else:b=l or rt or next(x for x in w if x)
    h=max([R.count(b)for R in i if 0 not in R]+[w.count(b)])
    v=max([sum(i[R][C]==b for R in range(H))for C in range(W)if all(i[R][C]for R in range(H))]+[sum(i[R][c]==b for R in range(H))])
    d=h==W and v<H or h>v or h==v and H>W
    if d:
     for j in range(H):
      if i[j][c]==b:g[j][c]=0
    else:
     for j in range(W):
      if w[j]==b:g[r][j]=0
 return g