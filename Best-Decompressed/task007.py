p=lambda g,R=range:[[max(sum(g,[])[(x+y)%3::3])for y in R(7)]for x in R(7)]
