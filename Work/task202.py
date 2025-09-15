def p(i):
 g=[r[:]for r in i]
 for r,w in enumerate(i):
  for c,v in enumerate(w):
   if v<1:
    l=w[c-1]if c>0 else None
    rt=w[c+1]if c<len(w)-1 else None

    # Determine background by checking all directions
    if l and rt and l!=rt:
     # Check all perpendicular directions with safe bounds checking
     up=i[r-1][c]if r>0 else None
     dn=i[r+1][c]if r<len(i)-1 else None
     lf=w[c-2]if c>1 else None
     rg=w[c+2]if c<len(w)-2 else None

     # Count votes from all perpendicular directions
     l_votes=sum(x==l for x in[up,dn,lf,rg]if x is not None)
     rt_votes=sum(x==rt for x in[up,dn,lf,rg]if x is not None)

     if l_votes>rt_votes:b=l
     elif rt_votes>l_votes:b=rt
     else:
      # Fallback to size-based heuristic
      lh,rh=w.count(l),w.count(rt)
      if abs(lh-rh)>2:b=rt if rh<lh else l
      else:b=l
    else:
     b=l if l else rt if rt else next(x for x in w if x)

    # Region size detection with pattern shape consideration
    h=0
    for rr in range(len(i)):
     if 0 not in i[rr]:h=max(h,i[rr].count(b))
    if h==0:h=w.count(b)

    v=0
    for cc in range(len(w)):
     if all(i[rr][cc]!=0 for rr in range(len(i))):
      v=max(v,sum(1 for rr in range(len(i))if i[rr][cc]==b))
    if v==0:v=sum(1 for rr in range(len(i))if i[rr][c]==b)

    # Consider overall pattern shape for decision
    pattern_tall=len(i)>len(i[0])
    if h==v:draw_vertical=pattern_tall
    else:draw_vertical=h>v

    if draw_vertical:
     for j in range(len(i)):
      if i[j][c]==b:g[j][c]=0
    else:
     for k in range(len(w)):
      if w[k]==b:g[r][k]=0
 return g