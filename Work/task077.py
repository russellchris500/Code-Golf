def p(g):
 m=[*zip(*g)];h=len(g);w=len(g[0]);e=range
 for t in e(h):
  if 2 in g[t]:
   for b in e(t+1,h):
    if 2 in g[b]:
     for l in e(w):
      if 2 in m[l]:
       for r in e(l+1,w):
        if 2 in m[r]:
         if 0 not in {g[x][y]for x in e(t,b+1) for y in e(l,r+1)} and all([2 in i for i in g[t:b+1]]) and all([2 in i for i in m[l:r+1]]):
          for x in e(t,b+1):
           for y in e(l,r+1):
            if g[x][y] not in {0,2}:g[x][y]=4
 return g