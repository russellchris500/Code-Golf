def p(g):
 v=lambda k:0<=k<W*(W-1)and k%W<W-1 and g[k//W][k%W];g=[[c or 4 for c in r]for r in g];W=len(g)+1
 for i in range(W*W*W):
  k=i%(W*W)
  if v(k)==4 and not v(k-1)*v(k+1)*v(k-W)*v(k+W):g[k//W][k%W]=0
 return g
