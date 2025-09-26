q=lambda g:([*map(any,g)].index(1),[*map(any,zip(*g))].index(1))
h=[[(0,0),(0,4),(4,0),(4,4)],[(0,2),(2,4),(4,2),(2,0)],[(1,1),(1,3),(3,3),(3,1)]]
p=lambda g:[[(s:=[]),max(s:=s+g[[*map(any,g)].index(1)+x][[*map(any,zip(*g))].index(1)+y])for x,y in i*2] for i in h]