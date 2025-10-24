from collections import*
def p(t,l=range):
 g=[[0]*10for o in l(10)]
 for o in l(10):
  for r in l(10):
   if t[o][r]and not g[o][r]:
    j=deque([(o,r)]);g[o][r]=1;n=[]
    while j:
     f,i=j.popleft();n.append((f,i))
     for(m,u)in((1,0),(-1,0),(0,1),(0,-1)):
      a,c=f+m,i+u
      if 0<=a<10and 0<=c<10and not g[a][c]and t[a][c]:g[a][c]=1;j.append((a,c))
    c=2if len(n)==6else 1
    for(f,i)in n:t[f][i]=c
 return t