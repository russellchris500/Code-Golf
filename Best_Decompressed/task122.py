q=lambda g:[r[-2:][::(-1)**len(r)]+r[:-2]for r in g]
p=lambda g:sum(map(any,g))<4and q(g)or[*zip(*q(zip(*g)))]
