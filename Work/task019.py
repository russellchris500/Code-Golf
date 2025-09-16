def p(g):
    h,w=len(g),len(g[0])
    r=[[g[i//2][j//2]for j in range(w*2)]for i in range(h*2)]
    o=[row[:]for row in r]
    for i in range(h*2):
        for j in range(w*2):
            if r[i][j]==0:
                for di,dj in(-1,-1),(-1,1),(1,-1),(1,1):
                    ni,nj=i+di,j+dj
                    if 0<=ni<h*2 and 0<=nj<w*2 and r[ni][nj]not in(0,8):
                        o[i][j]=8
                        break
    return o