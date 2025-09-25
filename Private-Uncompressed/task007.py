def p(i):
 g=[x for r in i for x in r]
 c=[max(g[j::3])for j in range(3)]
 n=len(i)
 return[[c[(r+k)%3]for k in range(n)]for r in range(n)]