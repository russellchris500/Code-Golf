def p(g):
 h,w=len(g),len(g[0])
 o=[r[:]for r in g]
 p=None
 best=0
 for i in range(h-2):
  for j in range(w-2):
   count=sum(g[r][c]not in[0,5]for r in range(i,i+3)for c in range(j,j+3))
   if count>best:
    best=count
    p=[[g[r][c]for c in range(j,j+3)]for r in range(i,i+3)]
 for i in range(h):
  for j in range(w):
   if g[i][j]==5:
    for di in range(-1,2):
     for dj in range(-1,2):
      ni,nj=i+di,j+dj
      if 0<=ni<h and 0<=nj<w and p:
       o[ni][nj]=p[di+1][dj+1]
    break
 return o