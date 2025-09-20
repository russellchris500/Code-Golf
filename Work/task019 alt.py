# this solution is 214 char vs submitted is 207 char. This one is much easier to read.
def p(g):
 g=[r*2 for r in g*2];h=len(g);w=len(g[0])
 def s(x,y):
  if h>x>=0<=y<w>g[x][y]<1:g[x][y]=8
  for a in range(h*w):
   x=a%h;y=a//h
   if g[x][y]%8>0:s(x+1,y+1);s(x+1,y-1);s(x-1,y+1);s(x-1,y-1)
  return g