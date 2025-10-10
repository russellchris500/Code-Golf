def r(g):
 o=[]
 for y,w in enumerate(g):
  c=0
  for x,v in enumerate(w):
   if v>8:c=c and[c[0]+[(x,y)],c[1]+1]or[[(x,y)],1]
   elif c:o+=[c];c=0
   if v<1and 9in[*zip(*g)][x][:y]:g[y][x]=1
  if c:o+=[c]
 return o
def p(g):s=r(g);[[g[y].__setitem__(x,3)for x,c in enumerate(w)for l in s for a,b in l[0]if max(abs(x-a),abs(y-b))<=l[1]//2and c!=9]for y,w in enumerate(g)];return g