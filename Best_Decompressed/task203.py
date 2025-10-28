p=lambda g:[[dict(zip(g[L:=len(g)//2][:L],g[L][L:]))[p]for p in r]for r in g]
