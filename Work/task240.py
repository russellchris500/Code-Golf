def p(g):
 h=[[*r] for r in g];R=range
 for o in R(1,8,2):
  e=18-o
  for r in R(o,e+1,2):
   for c in R(o,e+1,2):h[r][c]=max(g[o][o+2],g[o][e-2],g[e][o+2],g[e][e-2])
  h[o][o]=h[o][e]=h[e][o]=h[e][e]=max(g[o][o],g[o][e],g[e][o],g[e][e])
 return h