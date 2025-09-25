def p(g):
 x,y=divmod(sum(g,[]).index(8),len(g[0]));c=[r[y-1:y+2] for r in g[x-1:x+2]];c[1][1]=0;c[1][1]=max(max(*c));return c