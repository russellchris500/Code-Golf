p=lambda g:([(r[1:3+(r[0]==r[3])]*10)[:len(g)]for r in g[:2+(g[0]==g[3])]]*10)[:len(g)]
