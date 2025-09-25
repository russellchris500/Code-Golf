def p(g):
 n,t=(len(g))//2,g[0][(len(g))//2];q=[[t if g[i][j]and g[i][j]!=t else 0 for j in range(n)]for i in range(n)];return[q[i]+q[i][::-1]for i in range(n)]+[q[~i]+q[~i][::-1]for i in range(n)]
