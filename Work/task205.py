def p(g):
 h,w=len(g),len(g[0])
 for a in range(h*w,3,-1):
  for rh in range(2,h+1):
   if a%rh!=0:continue
   rw=a//rh
   if rw<2 or rw>w:continue
   for i in range(h-rh+1):
    for j in range(w-rw+1):
     l=[g[r][c]for r in range(i,i+rh)for c in range(j,j+rw)]
     if len(set(l))==2:
      b=max(set(l),key=l.count)
      o=[[b]*rw for _ in range(rh)]
      for r in range(i,i+rh):
       for c in range(j,j+rw):
        o[r-i][c-j]=g[r][c]
      for r in range(i,i+rh):
       for c in range(j,j+rw):
        if g[r][c]!=b:
         for y in range(rh):o[y][c-j]=g[r][c]
         for x in range(rw):o[r-i][x]=g[r][c]
      return o
 return g