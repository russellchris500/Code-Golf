def p(g):
 o=[[0]*9 for _ in range(9)]
 r=0
 for i in range(2):
  for j in range(2):
   if g[i][j]==2:r=i*2+j
   if g[i][j]==3:
    for x in range(3):
     for y in range(3):
      o[i*3+x][j*3+y]=3
      o[(1-i)*3+x][(1-j)*3+y]=3
 return o