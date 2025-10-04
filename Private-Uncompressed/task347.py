def p(j,A=range(3)):
 for b in A:
  for c in A:
   j[b][c]=6*(j[b][c]+j[b][c+3]>0)
 return[j[:3]for j in j]