def p(g):
 h=range(len(g));s=set();g=[[c or 4 for c in r]for r in g]
 for i in h:s|={(-1,i),(len(g),i),(i,-1),(i,len(g))}
 for _ in range(40):
  for x in h:
   for y in h:
    n={(x,y+1),(x,y-1),(x+1,y),(x-1,y)}
    if g[x][y]>3 and n&s:g[x][y]=0;s|={(x,y)}
 return g
 

   