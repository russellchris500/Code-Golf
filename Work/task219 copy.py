def p(x):
 a=[r[:]for r in x];H,W=len(a),len(a[0])
 s=lambda y,x:((y+d,x+e)for d in(-1,0,1)for e in(-1,0,1)if(d|e)and 0<=y+d<H and 0<=x+e<W)
 def comps():
  v=set();D=[]
  for y in range(H):
   for x in range(W):
    if a[y][x]==8and(y,x)not in v:
     q={(y,x)};R=set()
     while q:
      p=set()
      for i,j in q:
       if(i,j)not in v and a[i][j]==8:v.add((i,j));R.add((i,j));p|=set(s(i,j))
      q=p-v
     D.append(tuple(sorted(R)))
  return D
 M=lambda E:min(i for i,_ in E)
 K=lambda E:(M(E),min(j for _,j in E))
 t=sorted(comps(),key=lambda z:(M(z),K(z)[1]))
 if not t:return a
 w=M(t[0])
 for y in range(w+1,H):
  if any(a[y][x]for x in range(W)):w=y
  elif w>=M(t[0]):break
 V=set()
 for E in t:
  if M(E)<=w:V|=set(E)
  else:break
 if not V:return a
 r0=min(i for i,_ in V);c0=min(j for _,j in V)
 z=[(i-r0,j-c0)for i,j in sorted(V)]
 def bands(L):
  B=[];cur=None;bot=-1
  for E in L:
   m=M(E)
   if m>w:
    k=max(i for i,_ in E)
    if cur is None or m>bot+1:cur is not None and B.append(tuple(sorted(cur)));cur=set(E);bot=k
    else:cur|=set(E);bot=max(bot,k)
  cur is not None and B.append(tuple(sorted(cur)))
  return B
 J=[]
 for E in bands(t):
  T=K(E);B=set(E);A=[{(i+T[0]+d,j+T[1]+e)for i,j in z}for d,e in[(0,2),(0,1),(0,0),(0,-1),(0,-2),(-1,0)]];m=max([(Q,len(Q&B),min(i for i,_ in Q)if Q else 9e9)for Q in A],key=lambda k:(k[1],-k[2]));J.append((m[0]if m[1]else B,max(j for _,j in E)))
 R=[r[:]for r in a]
 for P,cut in J:
  for y,x in P:
   if x>cut and 0<=y<H and 0<=x<W and R[y][x]==0:R[y][x]=1
 return R