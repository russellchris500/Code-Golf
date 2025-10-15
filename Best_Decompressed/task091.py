def p(g):s=[r for r in g if 5in r];t=s[0];i=g.index(t);q=t.index(5);return[x[q:-~t.index(5,q+1)]for x in g[i-1:i-~len(s)]]
