def p(g):c=[*map(len,[set(r)for r in g])].index(1)+1;return[r[-1::-c]for r in g[::c]]
