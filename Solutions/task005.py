def p(g):
 h,w,q=len(g),len(g[0]),[*zip(*g)];x=y=0
 for r in range(1,h-1):
  for c in range(1,w-1):
   if max(g[r-1][c-1:c+2])==max(g[r+1][c-1:c+2])==max(q[c-1][r-1:r+2])==max(q[c+1][r-1:r+2])!=0:x,y=r,c;break
  if x:break
 o=[[0]*w for _ in range(h)];t=[[g[x+i-1][y+j-1]if 0<=x+i-1<h and 0<=y+j-1<w else 0 for j in range(3)]for i in range(3)];d=[]
 for i in[-1,0,1]:
  for j in[-1,0,1]:
   if i|j==0:continue
   f=next((g[x-1+i*4+u][y-1+j*4+v]for u in range(4)for v in range(4)if 0<=x-1+i*4+u<h and 0<=y-1+j*4+v<w and g[x-1+i*4+u][y-1+j*4+v]),0)
   if f:d.append((i,j,f))
 for i in range(3):
  for j in range(3):
   if 0<=x-1+i<h and 0<=y-1+j<w:o[x-1+i][y-1+j]=t[i][j]
 for i,j,f in d:
  k=1
  while x-1+i*4*k+2>=0 and x-1+i*4*k<h and y-1+j*4*k+2>=0 and y-1+j*4*k<w:
   for u in range(3):
    for v in range(3):
     if t[u][v]and 0<=x-1+i*4*k+u<h and 0<=y-1+j*4*k+v<w:o[x-1+i*4*k+u][y-1+j*4*k+v]=f
   k+=1
 return o