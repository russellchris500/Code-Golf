def p(g):
 h,w=len(g),len(g[0])
 v=[[0]*w for _ in range(h)]
 rs=[]
 for r in range(h):
  for c in range(w):
   if not v[r][c]and g[r][c]in[1,2]:
    s,cs,rc=[(r,c)],[],0
    while s:
     x,y=s.pop()
     if x<0 or x>=h or y<0 or y>=w or v[x][y]or g[x][y]==0:continue
     v[x][y]=1
     cs.append((x,y))
     rc+=g[x][y]==2
     for dx,dy in[(0,1),(1,0),(0,-1),(-1,0)]:
      if 0<=x+dx<h and 0<=y+dy<w and not v[x+dx][y+dy]and g[x+dx][y+dy]in[1,2]:s.append((x+dx,y+dy))
    if cs:
     r1,r2=min(r for r,c in cs),max(r for r,c in cs)
     c1,c2=min(c for r,c in cs),max(c for r,c in cs)
     rs.append((rc,r1,r2,c1,c2))
 _,r1,r2,c1,c2=max(rs)
 return[[g[r][c]for c in range(c1,c2+1)]for r in range(r1,r2+1)]