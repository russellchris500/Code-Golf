def p(g):
   w,h=len(g[0]),len(g)
   i,j = divmod([v for r in g for v in r].index(3),w)
   o=[r[:j+1]+r[j::-1]for r in g[:i+1]];o+=o[::-1]    
   f=[r[:w] for r in o[:h]]
   return [r+[0]*(w-len(r)) for r in f]+[[0]*w]*(h-len(f))