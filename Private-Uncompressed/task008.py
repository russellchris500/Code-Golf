def p(g):
 for _ in[1]*4:e=[*enumerate(g)];b=max(i for i,r in e if 2in r);d=min(i for i,r in e if 8in r);g=[*zip(*((d>b)*(d+~b)*[[0]*len(g[0])]+[g[:b+1]+g[d:],g][d<=b]))][::-1]
 return g