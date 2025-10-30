def p(h):
 n=len(h);F=lambda l,u:{(r,c)for r,R in enumerate(l)for c,v in enumerate(R)if v==u};v=F(h,1);g=F(h,4)
 if not v:return h
 r0=min(r for r,c in v);c0=min(c for r,c in v);t=tuple(tuple(h[r][c0:max(c for r,c in v)+1])for r in range(r0,max(r for r,c in v)+1));A=lambda x:tuple(zip(*x[::-1]));R=[t,A(t),tuple(r[::-1]for r in t[::-1]),A(A(A(t)))];R+=[tuple(r[::-1]for r in x)for x in R[:4]];z=set()
 for T in R:
  y=F(T,4);w=F(T,1)
  if y and w:
   a,b=min(r for r,c in y),min(c for r,c in y);d,e=min(r for r,c in w),min(c for r,c in w);Y={(r-a,c-b)for r,c in y};W={(r-d,c-e)for r,c in w};s=-~max(r for r,c in Y);x=-~max(c for r,c in Y)
   for i in range(n-s+1):
    for j in range(n-x+1):
     if{(r,c)for r,c in g if i<=r<i+s and j<=c<j+x}=={(r+i,c+j)for r,c in Y}:z|={(r+i+d-a,c+j+e-b)for r,c in W}
 return tuple(tuple(1if(r,c)in z else h[r][c]for c in range(n))for r in range(n))
