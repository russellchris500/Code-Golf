def q(g):
 r=[row[:]for row in g]
 n=len(g)
 for i in range(n):
  row=r[i]
  for c in range(1,10):
   pos=[j for j in range(n)if row[j]==c]
   if len(pos)>=4:
    l,r_pos=min(pos),max(pos)
    for j in range(l,r_pos+1):r[i][j]=c
 return r
def p(g):
 n=len(g)
 # Remove grid lines
 no_grid=[[g[i][j]for j in range(n)if j%3!=2]for i in range(n)if i%3!=2]
 # Process rows
 rows_done=q(no_grid)
 # Transpose original no-grid data for columns
 cols_input=[[no_grid[j][i]for j in range(len(no_grid))]for i in range(len(no_grid[0]))]
 cols_done=q(cols_input)
 # Transpose back
 cols_back=[[cols_done[j][i]for j in range(len(cols_done))]for i in range(len(cols_done[0]))]
 # Combine results
 combined=[[max(rows_done[i][j],cols_back[i][j])for j in range(len(rows_done[0]))]for i in range(len(rows_done))]
 # Add grid lines back
 r=[[0]*n for _ in range(n)]
 ri=rj=0
 for i in range(n):
  if i%3==2:
   for j in range(n):r[i][j]=g[i][j]
  else:
   rj=0
   for j in range(n):
    if j%3==2:r[i][j]=g[i][j]
    else:r[i][j]=combined[ri][rj];rj+=1
   ri+=1
 return r