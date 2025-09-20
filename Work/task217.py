def p(g):
 n=[(i,j)for i in range(9)for j in range(9)if g[i][j]]
 if not n:return g
 r1,r2,c1,c2=min(r for r,c in n),max(r for r,c in n),min(c for r,c in n),max(c for r,c in n)
 t=[[g[r][c]for c in range(c1,c2+1)]for r in range(r1,r2+1)]
 o=[[0]*9 for _ in range(9)]
 for i in range(len(t)):
  for j in range(len(t[0])):
   if t[i][j]:
    for x in range(len(t)):
     for y in range(len(t[0])):
      if 0<=i*3+x<9 and 0<=j*3+y<9:o[i*3+x][j*3+y]=t[x][y]
 return o