def p(g,R=range,L=len):
 a=sum(g,[])
 B=max(a,key=a.count);S=max([v for v in a if v!=B],key=a.count)
 h,w=L(g),L(g[0]);t={};P=set();M=set()
 for i in R(h):
  for j in R(w):
   if (c:=g[i][j])not in(B,S):
    P.add(i+j);M.add(i-j);t.setdefault(c,0)
    for y,x in((1,0),(-1,0),(0,1),(0,-1)):
     Y,X=i+y,j+x
     if 0<=Y<h and 0<=X<w:t[c]+=(g[Y][X]==B)-(g[Y][X]==S)
 U=set(t);b=max(U,key=t.get);o=sum(U)-b;r=[*map(list,g)]
 for i in R(h):
  for j in R(w):
   v=g[i][j]
   if v in(B,S)and((i+j in P)or(i-j in M)):r[i][j]=b if v==B else o
 return r