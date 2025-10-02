def p(g):
 W=len(g)
 def f(i,j):
  if 0<=i<W>j>=0==g[i][j]:g[i][j]=1;f(i+1,j);f(i-1,j);f(i,j+1);f(i,j-1)
 for i in range(W):f(i,0);f(i,W-1);f(0,i);f(W-1,i)
 return[[(4,0,0,3)[a]for a in r]for r in g]
