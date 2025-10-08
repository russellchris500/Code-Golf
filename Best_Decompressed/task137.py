def p(g):R=range(len(g));p=[[i,j]for i in R for j in R if g[i][j]];x,y=p[1];return[[g[x][y]*(max(abs(i-y),abs(j-x))%(p[2][0]-x)<1)for i in R]for j in R]
