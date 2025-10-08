p=lambda g,E=enumerate,t=(-1,0,1):[[v*any((i|j)*sum(g[y+i:y+i+1]and g[y+i][x+j:x+j+1])for i in t for j in t)for x,v in E(r)]for y,r in E(g)]
