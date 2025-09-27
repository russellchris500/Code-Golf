def p(g):
 f=sum(g,[])
 a,*_=zip(*g)
 b=g[0]+[*a]
 t=next(x for x in {*b}-{0} if b.count(x)*2==f.count(x)==4)
 return [[t*(g[i][0]==t or g[0][j]==t) for j in range(len(g[0]))] for i in range(len(g))]
