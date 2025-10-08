def p(z):
 C=tuple(map(tuple,z));R=range;I,J=len(C),len(C[0]);v=[[0]*J for _ in R(I)];S=[];O=[]
 for i in R(I):
  for j in R(J):
   if v[i][j]:continue
   c,s,h=C[i][j],[(i,j)],set();v[i][j]=1
   while s:
    y,x=s.pop();h.add((y,x))
    for d,e in(1,0),(-1,0),(0,1),(0,-1):
     a,b=y+d,x+e
     if 0<=a<I and 0<=b<J and not v[a][b]and C[a][b]==c:v[a][b]=1;s.append((a,b))
   (O,S)[len(h)>1].append((c,h))
 if not S:return[list(r)for r in C]
 T={}
 for c,h in S:T[c]=T.get(c,0)+len(h)
 m=sorted(T,key=lambda k:(-T[k],k));g,k=m[0],(m[1]if len(m)>1else m[0]);X={(i,j)for i in R(I)for j in R(J)if C[i][j]==g};Y={(i,j)for i in R(I)for j in R(J)if C[i][j]==k};A=[(c,h)for c,h in O if c not in(g,k)]or O
 Z={(r,c)for _,h in A for y,x in h for d,e in((1,1),(-1,-1),(1,-1),(-1,1))for r,c in[(y+d*n,x+e*n)for n in R(max(I,J))]if 0<=r<I and 0<=c<J}
 E={}
 for c,_ in A:E[c]=E.get(c,0)+1
 L=sorted(E,key=lambda c:(-E[c],c));A1,B1=(L+[L[0]])[:2];M=lambda m:sum((C[y+d][x+e]==g)-(C[y+d][x+e]==k)for c,h in A if c==m for y,x in[next(iter(h))]for d in(-1,0,1)for e in(-1,0,1)if(d or e)and 0<=y+d<I and 0<=x+e<J);a,b=M(A1),M(B1);D,E=(A1,B1)if a>0and b<0else(B1,A1)if a<0and b>0else(B1,A1)if b>0else(A1,B1);e=[list(r)for r in C]
 for y,x in Z&X:e[y][x]=D
 for y,x in Z&Y:e[y][x]=E
 return e
