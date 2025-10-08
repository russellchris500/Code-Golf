q=lambda g:[g[[6*(a:=2in g[3]),7-2*a,6-6*a,3,4,5-3*a,0,0,0,9-9*(b:=2in g[11]),10,11,8-8*b,7+2*b,8*b][r]]for r in range(15)]
p=lambda g:[q(g),[*zip(*q([*zip(*g)]))]][sum([2 in r for r in g])>4]