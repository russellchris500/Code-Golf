from collections import*
def p(g):
 C=Counter(sum(g,[]));b=C.most_common()[0][0];m=max((c for c in C if c!=b),key=C.get);h=len(g);w=len(g[0]);B=0;V=0
 for t in C:
  if t in[b,m]:continue
  P=[(r,c)for r in range(h)for c in range(w)if g[r][c]==t]
  if P:
   r0,r1,c0,c1=min(r for r,_ in P),max(r for r,_ in P),min(c for _,c in P),max(c for _,c in P);O=[[g[r][c]for c in range(c0,c1+1)]for r in range(r0,r1+1)];H=r1-r0+1;W=c1-c0+1
   for sr in range(-2*H,h):
    for sc in range(-2*W,w):
     ok=v=hid=0;ok=1
     for r in range(H):
      for c in range(W):
       if O[r][c]==t:
        for i in range(4):
         x,y=sr+2*r+i//2,sc+2*c+i%2
         if 0<=x<h and 0<=y<w:ok*=g[x][y]==m;v+=1
         else:hid=1
     if ok*hid and v>V:B=O;V=v
 return B or[[b]]
