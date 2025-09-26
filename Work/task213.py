def p(g):
 h,w=len(g),len(g[0])
 gc=[(i,j)for i in range(h)for j in range(w)if g[i][j]==5]
 if not gc:return g
 s=max(r for r,c in gc)-min(r for r,c in gc)+1
 c=[]
 d='h'
 for i in range(h):
  u=list(dict.fromkeys([g[i][j]for j in range(w)if g[i][j]not in[0,5]]))
  if len(u)==s:c,d=u,'v';break
 if not c:
  for j in range(w):
   u=list(dict.fromkeys([g[i][j]for i in range(h)if g[i][j]not in[0,5]]))
   if len(u)==s:c,d=u,'h';break
 if not c:
  hs=[(i,next(iter(x)))for i in range(h)for x in[{g[i][j]for j in range(w)if g[i][j]not in[0,5]}]if len(x)==1]
  vs=[(j,next(iter(x)))for j in range(w)for x in[{g[i][j]for i in range(h)if g[i][j]not in[0,5]}]if len(x)==1]
  if len({x for p,x in vs})>len({x for p,x in hs})or(len({x for p,x in vs})==len({x for p,x in hs})and len(vs)>=len(hs)):
   c,d=[x for p,x in sorted(vs)],'v'
  else:
   c,d=[x for p,x in sorted(hs)],'h'
 return[[c[(i if d=='h'else j)%len(c)]for j in range(s)]for i in range(s)]