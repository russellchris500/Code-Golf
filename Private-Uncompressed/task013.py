def p(g):
 def f(m):
  h,w=len(m),len(m[0]);H,W=range(h),range(w)
  r=[[0]*w for _ in H]
  P=[(i,j,m[i][j])for i in H for j in W if m[i][j]]
  if len(P)==2:
   y1,x1,c1=P[0]
   y2,x2,c2=P[1]
   if(x1<1 or x1>w-2)&(x2<1 or x2>w-2):
    d=abs(y2-y1);n=min(y1,y2)
    for i in H:
     for j in W:
      if i>=n:
       p=(i-n)//d;q=(i-n)%d
       if q==y1-n:r[i][j]=[c1,c2][p%2]
       elif q==y2-n:r[i][j]=[c2,c1][p%2]
  return r
 
 s=f(g)
 if any(any(row)for row in s):return s
 t=[list(row)for row in zip(*g)]
 u=f(t)
 return[list(row)for row in zip(*u)]