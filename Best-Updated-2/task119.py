def p(g):
 h=len(g);w=len(g[0]);s=sum(g,[]);k=s.index(8);d=s[k+w-1]==8
 for a in-1,1:
  b=a-2*a*d;y=k//w;x=k%w
  while w>x+b>=0<=y+a<h:
   Y=y+a;X=x+b;R=g[Y];v=R[X]
   if v-2:y,x=Y,X;R[X]=v or 3
   if R==[2]*w:a=-a
   if all(2==r[X]for r in g):b=-b
 return g
