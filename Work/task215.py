def p(g):
 h=len(g)
 s=next((i for i in range(h-2)if any(g[i][j]for j in range(len(g[i])))),0)
 t=[g[s+i][:]for i in range(3)]
 return[t[(i-s)%3]for i in range(h)]