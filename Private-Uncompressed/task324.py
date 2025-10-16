def p(g,R=range):
 a=sum(g,[]);B=max(a,key=a.count);S=max([v for v in a if v!=B],key=a.count);h,w=len(g),len(g[0]);t={};P=[];M=[];r=[*map(list,g)]
 for i in R(h):
  for j in R(w):
   if(c:=g[i][j])not in(B,S):
    P+=[i+j];M+=[i-j];t[c]=t.get(c,0)
    for y,x in(1,0),(-1,0),(0,1),(0,-1):
     if 0<=i+y<h and 0<=j+x<w:t[c]+=(g[i+y][j+x]==B)-(g[i+y][j+x]==S)
 b=max(t,key=t.get);o=sum(t)-b
 for i in R(h):
  for j in R(w):
   if(v:=g[i][j])in(B,S)and(i+j in P or i-j in M):r[i][j]=(o,b)[v==B]
 return r
