def p(g):
 b={-1};W=len(g)
 for i in range(W**3):
  k=i%(W*W);c=k%W;v=g[k//W];b|={-c-1,W*W+c}
  if i==k:v[c]=v[c]or 4
  if v[c]>3and(c%~-W<1or{k-1,k+1,k-W,k+W}&b):v[c]=0;b|={k}
 return g
