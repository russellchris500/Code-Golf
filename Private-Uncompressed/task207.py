def p(g):
 c=[[[g[b+i][a+j]for j in range(2)]for i in range(2)]for a,b in[(0,0),(3,0),(0,3),(3,3)]]
 return[x for x in c if c.count(x)==1][0]