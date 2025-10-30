def p(g):
 b=sum(g,[]).count(0);i=10-b
 return[[g[y//3][x//3]and for x in range(b*3)]for y in range(b*3)]