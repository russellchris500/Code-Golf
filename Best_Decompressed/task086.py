def p(l,R=range):
 z=len(l[0]);g=[[0]*z for _ in R(z)]
 for a in R(1,z-3):
  for i in R(1,z-3):
   if l[a][i]and not l[a-1][i]and not l[a][i-1]:
    b,f=l[a][i],l[a+1][i+1];s=3+(l[a+2][i+2]!=b);d=s-2
    for r,c,x,y,v in[(a-d,a,0,s,b),(a+s,a+s+d,0,s,b),(a,a+s,-d,0,b),(a,a+s,s,s+d,b),(a,a+s,0,s,f),(a+1,a+s-1,1,s-1,b)]:
     for q in R(r,c):g[q][i+x:i+y]=[v]*(y-x)
 return g
