p=lambda g:[[(s:=[0,2,2,1,0,3,4,4,4,4][5*p+s])and[0,s>1or(c:=2+(r[i:].index(1)%2)*5),c,1,1][s]for i,p in enumerate(r)]for r in g if~(s:=0)|(c:=0)]
