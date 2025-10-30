def p(l,R=range):
 z=len(l[0]);g=[[0]*z for _ in R(z)]
 for a in R(1,z-3):
  for i in R(1,z-3):
   if l[a][i]and not l[a-1][i]and not l[a][i-1]:
    b,f=l[a][i],l[a+1][i+1];s=3+(l[a+2][i+2]!=b);d=s-2
    for r in R(a-d,a):g[r][i:i+s]=[b]*s
    for r in R(a+s,a+s+d):g[r][i:i+s]=[b]*s
    for r in R(a,a+s):g[r][i-d:i]=[b]*d;g[r][i+s:i+s+d]=[b]*d;g[r][i:i+s]=[f]*s
    for r in R(a+1,a+s-1):g[r][i+1:i+s-1]=[b]*(s-2)
 return g