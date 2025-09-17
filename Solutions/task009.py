q=lambda g,h,a:[[j or(b.pop()if(b:=set(r[:i])&set(r[i:])&a)else 0)for i,j in enumerate(s)]for r,s in zip(g,h)]
p=lambda g:[*zip(*q([*zip(*g)],[*zip(*q(g,g,(c:=set(range(1,10))-set([g[0][2]]))))],c))]