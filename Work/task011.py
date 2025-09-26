def p(i):
 for r in[0,4,8]:
  for c in[0,4,8]:
   if all(i[r+x][c+y]-8 for x in range(3)for y in range(3)if r+x<11>c+y-1):
    o=[[i[r+x//4][c+y//4]if r+x//4<11>c+y//4-1 else 0 for y in range(11)]for x in range(11)]
    for j in[3,7]:
     for k in range(11):o[j][k]=o[k][j]=5
    return o