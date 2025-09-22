f=lambda g:next((i,j)for i,r in enumerate(g)for j,v in enumerate(r)if v)
grid = [[0,0,0],[0,0,6],[7,8,9]]
print(f(grid))