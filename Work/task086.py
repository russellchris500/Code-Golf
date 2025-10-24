def p(l,R=range):
 z=len(l[0]);g=[[0]*z for _ in R(z)]
 for a in R(1,z-3):
  for i in R(1,z-3):
   if l[a][i]and not l[a-1][i]and not l[a][i-1]:
    b,f=l[a][i],l[a+1][i+1]
    s=3if l[a+2][i+2]==b else 4
    d=s-2
    for r in R(a-d,a):
     for c in R(i,i+s):g[r][c]=b
    for r in R(a+s,a+s+d):
     for c in R(i,i+s):g[r][c]=b
    for r in R(a,a+s):
     for c in R(i-d,i):g[r][c]=b
    for r in R(a,a+s):
     for c in R(i+s,i+s+d):g[r][c]=b
    for r in R(a,a+s):
     for c in R(i,i+s):g[r][c]=f
    for r in R(a+1,a+s-1):
     for c in R(i+1,i+s-1):g[r][c]=b
 return g
