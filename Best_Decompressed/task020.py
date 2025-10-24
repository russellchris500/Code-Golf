def p(o,r=enumerate):
 a=f=9**9;p=i=-1
 for h,j in r(o):
  for t,d in r(j):
   if d:a=min(a,h);p=max(p,h);f=min(f,t);i=max(i,t)
 u=a+p;l=f+i
 for h in range(a,p+1):
  for t in range(f,i+1):
   q=[(h,t),(u-h,t),(a+t-f,f+h-a),(a+i-t,f+p-h)]
   e=max(o[r][c]for r,c in q)
   for r,c in q:o[r][c]=e
 return o
