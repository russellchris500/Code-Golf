# def p(g):
#  h=len(g);w=len(g[0]);s=set();g=[[c or 4 for c in r]for r in g]
#  def f(x,y,s):
#   if h>x>=0<=y<w and g[x][y]==4 and(x,y)not in s:s|={(x,y)};g[x][y]=0;[f(x+i,y+j,s)for i,j in[(0,1),(1,0),(0,-1),(-1,0)]]
#  for b in range(h*w):
#   x=b//w;y=b%w
#   if x*y<1 or x>h-2 or y>w-2:f(x,y,s)
#  return g

def p(g):
 R=range;W=len(g);h=sum(g,[])
 def f(h):
  i=0;s=[]
  for c in h:
   q={k for k in s if{i-W,i-1}&{*k}};i+=1
   if c<1:s={*s,sum(q,(i-1,))}-q
  return s
 for i in f(h):
  if not{*R(W),*R(W*W-W,W*W),*R(0,W*W,W),*R(-1,W*W,W)}&{*i}:
   for j in i:g[j//W][j%W]=4
 return g