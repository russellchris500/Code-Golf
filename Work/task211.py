def p(g):
 h,w=len(g),len(g[0])
 t=[[r[::-1]for r in g[::-1]],g[::-1],[r[::-1]for r in g],g,[r[::-1]for r in g[::-1]],g[::-1]]
 return[[t[i//h*2+j//w][i%h][j%w]for j in range(w*2)]for i in range(h*3)]