def p(g):
 h=len(g);w=len(g[0]);s=set();g=[[c or 4 for c in r]for r in g]
 def f(x,y,s):
  if h>x>=0<=y<w and g[x][y]==4 and(x,y)not in s:s|={(x,y)};g[x][y]=0;[f(x+i,y+j,s)for i,j in[(0,1),(1,0),(0,-1),(-1,0)]]
 for b in range(h*w):
  x=b//w;y=b%w
  if x*y<1 or x>h-2 or y>w-2:f(x,y,s)
 return g