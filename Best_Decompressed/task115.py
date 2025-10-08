p=lambda g:[[x]for x in dict.fromkeys(sum(g,[]))]if g[0][0]==g[0][-1]else[[*dict.fromkeys(sum(g,[]))]]
