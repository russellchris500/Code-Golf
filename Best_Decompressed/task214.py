def p(g):exec("for a in range(3):\n for b in range(3):g[a][b+4]=g[~b][a];g[a][b+8]=g[~a][2-b]");return g
