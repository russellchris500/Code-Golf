def p(g):
 h=len(g)
 o=[r[:]for r in g]
 gr=next(i for i in range(h)if 5 in g[i])
 for i in range(h):
  for j,c in enumerate(g[i]):
   if c==2:
    for k in range(i+1 if i<gr else gr+1,gr if i<gr else i):o[k][j]=2
   elif c==1:
    if i<gr:
     for k in range(i):o[k][j]=1
    elif i>gr:
     for k in range(i+1,h):o[k][j]=1
 return o