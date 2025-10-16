def p(g):
 R=range;H=len(g);W=len(g[0]);b=0
 [b or(b:=z)for y in R(H-6)for x in R(W-6)for h in R(min(10,H-y),5,-1)for w in R(min(10,W-x),5,-1)if(z:=[[g[j][i]for i in R(x,x+w)]for j in R(y,y+h)])and len({*sum(z,[])})<3]
 return[[sorted(r+c,key=(r+c).count)[0]for*c,in zip(*b)]for r in b]

# def p(g):
#  # f finds the rectangle recursively. g:grid rows remaining, x: starting x coord, w:width, r: partially constructed rectangle
#  def f(g,x,w,r):
#   if len(g)<1 or len({*sum(s:=r+[g[0][x:x+w]],[])})>2:
#    if len(r)<6:return[]
#    return r
#   else:return f(g[1:],x,w,s)
#  o=0
#  for y in range(len(g)-5):
#   for x in range(len(g[0])-5):
#    for w in range(10,5,-1):
#     if not o:o=f(g[y:],x,w,[])
#  return o
# def p(g):
#  E=enumerate;R=range
#  print("")
#  # Find rectangle candidates in each row
#  c={(x,y,w)for y,r in E(g)for w in R(10,5,-1)for x in R(0,len(r)-w)if len({*r[x:x+w]})<3}
#  print(c)
#  return g