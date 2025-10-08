def p(g,R=range,L=len,S=sum,E=enumerate,Z=zip,D=divmod):
 I=[D(i,L(g[0]))for i,v in E(S(g,[]))if v];s=I[0][1]==I[1][1]
 g=s and [*map(list,Z(*g))]or g
 I=[D(i,L(g[0]))for i,v in E(S(g,[]))if v];(y,x),(Y,X)=I;m=X-x>>1;a=g[y][x];b=g[y][X];t=x+m
 g[y][x:t]=[a]*m;g[y][t+2:X+1]=[b]*m
 for i in R(y-2,y+3):g[i][t-1]=a;g[i][t+2]=b
 for i in(y-2,y+2):g[i][t]=a;g[i][t+1]=b
 return s and[*Z(*g)]or g
