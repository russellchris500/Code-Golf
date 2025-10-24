def p(f):
 d,p=len(f),len(f[0]);e=None;g=-1
 for o in range(2,min(9,d)+1):
  for n in range(2,min(9,p)+1):
   for b in range(0,d-o+1):
    for u in range(0,p-n+1):
     a=True
     for a in range(b,b+o):
      i=f[a]
      if any(i[o]!=0for o in range(u,u+n)):a=False;break
     if a and o*n>g:g=o*n;e=b,u,o,n
 if e:
  b,u,o,n=e
  for a in range(b,b+o):
   for o in range(u,u+n):f[a][o]=6
 return f
