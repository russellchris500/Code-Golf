q=lambda g:[[4 if not c else c for c in r]for r in g]
a=lambda g:[p for p in range(len(g[0]))if g[0][p]==0]
def f(g,x,y,v=1):
 s,d={(x,y)},0
 while s:s={(*p,)for x,y in s for p in[(x+1,y),(x-1,y),(x,y+1),(x,y-1)]if 0<=p[0]<len(g)and 0<=p[1]<len(g[0])and g[p[0]][p[1]]==v and not(g[p[0]].__setitem__(p[1],d))}
p=lambda g:f(q(g),0,a(g)[0],4)