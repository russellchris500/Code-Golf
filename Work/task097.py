# p=lambda g,E=enumerate:[[v*(sum(len(g)>y+i>=0<=x+j<len(r)>0<g[y+i][x+j]for i in(-1,0,1)for j in(-1,0,1))>1)for x,v in E(r)]for y,r in E(g)]
# def p(g):
#  print("")
#  for r in zip((e:=[[0]*30])+g,g,g[1:]+e):
#   for p in zip((f:=[[0]*3])+(z:=[*zip(*r)]),z,z[1:]+f):
#    print(p)
#   print("")
#  return g
# p=lambda g:[[sum(p,[]).count(0)<8and p[1][1]for p in zip(z,z[1:],z[2:])]for r in zip([[0]*30]+g,g,g[1:]+[[0]*30])if(z:=[[0]*3,*zip(*r),[0]*3])]
# import re
# p=lambda g:eval(re.sub(f"(<=0, 0, 0{{{len(g[0])}}}0, )","0",str(g)))
