def p(a):
 q,r,j,b=[21]*10,[21]*10,[-1]*10,[-1]*10
 for y in range(21):
  for x,k in enumerate(a[y]):q[k]=min(q[k],x);r[k]=min(r[k],y);j[k]=max(j[k],x);b[k]=max(b[k],y)
 for k in range(1,10):
  if j[k]-q[k]==b[k]-r[k]==2:X,Y=q[k],r[k];break
 O=[[0]*21 for _ in a];Z=[(x,y)for y in range(3)for x in range(3)if a[Y+y][X+x]]
 for y in range(3):O[Y+y][X:X+3]=a[Y+y][X:X+3]
 for dx,dy in[(x,y)for x in(-4,0,4)for y in(-4,0,4)if x|y]:
  if k:=next((a[Y+dy+y][X+dx+x]for y in range(3)for x in range(3)if 0<=Y+dy+y<21 and 0<=X+dx+x<21 and a[Y+dy+y][X+dx+x]),0):
   cx,cy=X,Y
   while-3<cx<21 and-3<cy<21:
    cx+=dx;cy+=dy
    for x,y in Z:
     if 0<=cy+y<21 and 0<=cx+x<21:O[cy+y][cx+x]=k
 return O
