def p(g):
 h=len(g);w=len(g[0]);F=sum(g,[]);k=min({*F},key=F.count)
 s=h;u=w;t=-1;C=set();E=enumerate;R=range
 for i,r in E(g):
  for j,a in E(r):(a==0 and(C.add((i,j)),s>i and(s:=i),t<i and(t:=i),u>j and(u:=j)))or(a==k and(y:=i,x:=j))
 m=t-s+1;A=(s+t)//2;B=(2*u+m-1)//2;S=lambda z:(z>0)-(z<0);r=m*S(y-A);c=m*S(x-B)
 H=all((s+i,u+i)in C for i in R(m))or all((s+i,u+m-1-i)in C for i in R(m))
 P=len(C)==4*m-4
 if not(P or H):r-=S(r);c-=S(c)
 B=[(i-s,j-u)for i,j in C];y=s;x=u
 while 1:
  y+=r;x+=c;q=0
  for a,b in B:
   i=y+a;j=x+b;h>i>=0<=j<w and(g[i].__setitem__(j,k),q:=1)
  if not q:break
 return g