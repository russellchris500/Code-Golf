def p(p):
 b,b=len(p),len(p[0]);a={(r,c)for r in range(b)for c in range(b)if p[r][c]==3};t={*()}
 for k in[3,2,1]:
  for r in range(b):
   for c in range(b):
    for P in[0,1]:
     f,l,e,c3=(c+k,c,c-k,c+2*k)if P else(c,c+k,c+2*k,c-k);n={*()}
     for d in range(k):
      for q in range(k):
       if 0<=r+d<b and 0<=f+q<b:n.add((r+d,f+q))
       if 0<=r+d+k<b and 0<=l+q<b:n.add((r+d+k,l+q))
     if len(n)==2*k*k and n<=a and not n&t:
      t|=n
      for d in range(k):
       for q in range(k):
        if 0<=r+d-k<b and 0<=e+q<b:p[r+d-k][e+q]=8
        if 0<=r+d+2*k<b and 0<=c3+q<b:p[r+d+2*k][c3+q]=8
 return p
