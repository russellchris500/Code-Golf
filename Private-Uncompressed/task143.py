d=range
def p(y):
 f=len(y);n=[(q,s)for q in d(3)for s in d(3)if y[q][s]];Q,S=n[0]
 for e in d(f-2):
  for m in d(e<1,f-2):
   o=y[e+Q][m+S]
   if o*all(y[e+q][m+s]==o if(q,s)in n else not y[e+q][m+s]for q in d(3)for s in d(3))*all(not(0<=e+q+a<f and 0<=m+s+b<f and not(e<=e+q+a<e+3and m<=m+s+b<m+3)and y[e+q+a][m+s+b]==o)for q,s in n for a,b in((1,0),(-1,0),(0,1),(0,-1))):
    for q,s in n:y[e+q][m+s]=5
    return y