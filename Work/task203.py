def p(i):
 h,w=len(i),len(i[0])
 r=[[0]*w for _ in range(h)]
 for y in range(h):
  for x in range(w):
   d=min(x,y,w-1-x,h-1-y)
   for a in range(h):
    for b in range(w):
     if min(b,a,w-1-b,h-1-a)==min(h,w)//2-1-d:r[y][x]=i[a][b];break
 return r