def p(g):
 R=range(10);S=range(-10,10)
 n,p=[{(r,c)for r in R for c in R if g[r][c]==p}for p in(0,2)]
 o=[{(x+r,y+c)for x,y in p}for r in S for c in S]
 [exec("for x,y in i:g[x][y]=2")for i in o if i==i&n and{(1,3),(1,6)}-i and{(5,2),(6,3)}-i and{(3,6),(4,7),(3,8)}-i]
 return g