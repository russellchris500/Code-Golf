p=lambda g:[h for h in [g[:3],g[3:6],g[6:9]]if h!=[*map(list,zip(*h))]][0]
