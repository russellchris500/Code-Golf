# def p(g):
#  b={-1};W=len(g)
#  for i in range(W**3):
#   k=i%(W*W);c=k%W;v=g[k//W];b|={-c-1,W*W+c}
#   if i==k:v[c]=v[c]or 4
#   if v[c]>3and((c+1)%W<2or b&{k-1,k+1,k-W,k+W}):v[c]=0;b|={k}
#  return g
#
# def p(g):
#  v=lambda k:0<=k<W*(W-1)and k%W<W-1 and g[k//W][k%W];g=[[c or 4 for c in r]for r in g];W=len(g)+1
#  for i in range(W*W*W):
#   k=i%(W*W)
#   if v(k)==4 and not v(k-1)*v(k+1)*v(k-W)*v(k+W):g[k//W][k%W]=0
#  return g

def p(g):
 b={-1};W=len(g)
 for i in range(W**3):
  k=i%W**2;c=k%W;v=g[k//W];b|={-c-1,W*W+c}
  if i==k:v[c]=v[c]or 4
  if v[c]>3and(c%~-W<1or b&{k-1,k+1,k-W,k+W}):v[c]=0;b|={k}
 return g