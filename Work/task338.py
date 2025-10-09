# States:0-outside,1-inside,2-leading blue,3-trailing blue
# p=lambda g:[[(s:=[0,1,1,0,2,3,3,3][2*p+s])and[0,3,0,0][s]for i,p in enumerate(r)]for r in g if~(s:=0)]
p=lambda g:[[(s:=[0,1,1,0,2,3,3,3][2*p+s])and(s==1)*3for i,p in enumerate(r)]for r in g if~(s:=0)]