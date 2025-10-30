p=lambda g,R=(0,1,2):[[(l%2)*(l<sum(sum(g,[]))//4)for x in R if[l:=y*3+x+1]]for y in R]
