# p=lambda g,E=enumerate:[[v*(sum(len(g)>y+i>=0<=x+j<len(r)>0<g[y+i][x+j]for i in(-1,0,1)for j in(-1,0,1))>1)for x,v in E(r)]for y,r in E(g)]
# p=lambda g,R=range,L=len:[[g[y][x]*(sum(L(g)>(i:=y+k//3-1)>=0<=(j:=x+k%3-1)<L(g[0])>0<g[i][j]for k in R(9))>1)for x in R(L(g[0]))]for y in R(L(g))]
def p(g):
 for r in zip([[0]*30]+g,g,g[1:]+[[0]*30]):
  print(r)
 return g