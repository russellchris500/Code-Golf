# def p(g):
#  h=len(g);w=len(g[0]);s=set();g=[[c or 4 for c in r]for r in g]
#  def f(x,y,s):
#   if h>x>=0<=y<w and g[x][y]==4 and(x,y)not in s:s|={(x,y)};g[x][y]=0;[f(x+i,y+j,s)for i,j in[(0,1),(1,0),(0,-1),(-1,0)]]
#  for b in range(h*w):
#   x=b//w;y=b%w
#   if x*y<1 or x>h-2 or y>w-2:f(x,y,s)
#  return g

def p(g):
 h=range(len(g));s=set();g=[[c or 4 for c in r]for r in g]
 for i in h:s|={(-1,i),(len(g),i),(i,-1),(i,len(g))}
 for _ in range(40):
  for x in h:
   for y in h:
    n={(x,y+1),(x,y-1),(x+1,y),(x-1,y)}
    if g[x][y]>3 and n&s:g[x][y]=0;s|={(x,y)}
 return g