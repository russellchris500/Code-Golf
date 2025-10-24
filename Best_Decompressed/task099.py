def p(r,R=range):
 k,f=len(r),len(r[0]);m=[e[:]for e in r]
 for i in R(k):
  for j in R(f-4):
   if r[i][j:j+5]==[1,1,0,1,1]:
    h=1
    while i+h<k and r[i+h][j]:h+=1
    s=max(max(r[a][j+1:j+4])for a in R(i,i+h))
    for a in R(max(0,i-1),i+h):
     for b in R(j,j+5):
      if m[a][b]<1:m[a][b]=s
 return m
