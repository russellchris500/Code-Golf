def p(g):
 F=[(i//9,i%9)for i in range(81)if g[i//9][i%9]==4]
 for T in[[(i,j)for i,j in F if i+j<8],[(i,j)for i,j in F if i+j>=8]]:
  if T:I,J=zip(*T);[[g[i].__setitem__(j,7)for j in range(min(J),max(J)+1)if g[i][j]<1]for i in range(min(I),max(I)+1)]
 return g