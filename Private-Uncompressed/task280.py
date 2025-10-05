def p(g,R=range,L=len,E=enumerate,D=divmod,S=sum):
 H,W=L(g),L(g[0]);c=lambda y,x,r,s,n=0:n if not(0<=y<H and 0<=x<W and g[y][x]==3)else c(y+r,x+s,r,s,n+1)
 for y,x in[D(i,W)for i,v in E(S(g,[]))if v==2]:
  r=(y>0and g[y-1][x]==0and-1)or(y+1<H and g[y+1][x]==0and 1)or 0
  s=(not r and((x>0and g[y][x-1]==0and-1)or 1))
  a=c(y-r,x-s,-r,-s);b=c(y,x-1,0,-1);d=c(y,x+1,0,1);e=c(y-1,x,-1,0);f=c(y+1,x,1,0)
  n=min(a+1,(r and b+d+1)or(e+f+1))-1
  for k in R(-n,n+1):
   if r and 0<=x+k<W:
    for i in(r<0 and R(y,-1,-1)or R(y,H)):g[i][x+k]=3-(k==0)
   elif s and 0<=y+k<H:
    for j in(s<0 and R(x,-1,-1)or R(x,W)):g[y+k][j]=3-(k==0)
 return g