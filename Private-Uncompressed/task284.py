def p(g):
 indices = [divmod(i,len(g[0]))for i,v in enumerate(sum(g,[]))if v]
 same_col=indices[0][1]==indices[1][1]
 g=same_col*[*zip(*g)]+(1-same_col)*g
 indices_transposed=same_col*[*zip(*indices)]+(1-same_col)*indices
 dist = indices_transposed[1][1]-indices_transposed[0][1]
 g[indices_transposed[0][0]][indices_transposed[0][1]:indices_transposed[0][1]+(dist-1)//2] = [g[indices_transposed[0][0]][indices_transposed[0][1]]]*((dist-1)//2)
 g[indices_transposed[0][0]][indices_transposed[0][1]+((dist-1)//2)+2:indices_transposed[1][1]+1] = [g[indices_transposed[0][0]][indices_transposed[1][1]]]*((dist-1)//2)
 
 return g
test = [[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[9,0,0,0,0,0,0,0,0,8],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0]]
print(p(test))