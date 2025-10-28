#q=lambda g:[r for r in range(len(g)) if sum(set(g[r]))<2][1] #q is the size of the tile
#a=lambda g,b:[[sum({i for r in g[x::b]for i in r[y::b]})for x in range(b)]for y in range(b)] # a is a single tile
#p=lambda g:[(r*9)[:len(g)] for r in (a(g,q(g))*9)[:len(g)]] # tile 9x9 then slice
#p=lambda g:[(r*9)[:len(g)]for b in[[r for r in range(len(g))if sum(set(g[r]))<2][1]]for r in([[sum({i for r in g[x::b]for i in r[y::b]})for x in range(b)]for y in range(b)]*9)[:len(g)]]
q=lambda g:g[1][1:].index(1)+1