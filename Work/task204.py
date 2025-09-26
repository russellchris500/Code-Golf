def p(i):
 h,w=len(i),len(i[0])
 o=[r[:]for r in i]
 R=[]
 for a in range(h):
  for b in range(w):
   if i[a][b]:
    for c in range(a+2,h):
     for d in range(b+2,w):
      if i[c][d]and all(i[y][b]and i[y][d]for y in range(a,c+1))and all(i[a][x]and i[c][x]for x in range(b,d+1))and all(i[y][x]==0 for y in range(a+1,c)for x in range(b+1,d)):R+=(a,b,c,d),
 for a,b,c,d in R:
  s=int(((c-a-1)*(d-b-1))**0.5)
  for y in range(a+1,c):
   for x in range(b+1,d):o[y][x]=7 if s%2 else 2
 return o