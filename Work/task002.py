# p=lambda u:[u:=[[p%(a+4)or l for p,a in zip(r,[0]+r)]for*r,in zip(*u[::-1])]for l in[4]+[0]*79][-1]
p=lambda u,k=79:-k*u or p([[p%(a+4)or(k>78)*4for p,a in zip(r,[0]+r)]for*r,in zip(*u[::-1])],k-1)