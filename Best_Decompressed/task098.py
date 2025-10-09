p=lambda g,E=enumerate:[[0 if 0<r<len(g)-1and 0<c<len(g[0])-1and g[r][c-1]*g[r][c+1]*g[r-1][c]*g[r+1][c]>0 else g[r][c]for c,_ in E(R)]for r,R in E(g)]
