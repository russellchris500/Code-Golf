def p(g):
 b=sum(sum(g[-2:],[]))==3
 return b*[g[-2],g[-1],*g[:-2]]+(1-b)*[[r[-2],r[-1]]+r[:-2]for r in g]