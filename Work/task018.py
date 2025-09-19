def f(g,x,y,s,t,v):
 if len(g)>x>=0<=y<len(g[0])and g[x][y]==v and(x,y)not in t:s|={(x,y)};t|={(x,y)};[f(g,x+i,y+j,s,t,v)for i,j in[(0,1),(1,0),(0,-1),(-1,0)]]
 
def a(g,v,u):
 h=len(g);w=len(g[0]);t=set()
 def f(x,y,s):
  if h>x>=0<=y<w and g[x][y]and(x,y)not in t:s|={(x,y)};t|={(x,y)};[f(x+i,y+j,s)for i,j in[(0,1),(1,0),(0,-1),(-1,0)]]
 