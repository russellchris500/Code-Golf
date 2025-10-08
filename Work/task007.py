# def p(g):
#  x=([max(sum(g,[])[i::3])for i in(0,1,2)]*17)[:-2]
#  return [*zip(*[iter(x)]*7)]
p=lambda g,R=range:[[max(sum(g,[])[(x+y)%3::3])for y in R(7)]for x in R(7)]
#p=lambda g:[*zip(*[iter(([max(sum(g,[])[i::3])for i in(0,1,2)]*17)[:-2])]*7)]