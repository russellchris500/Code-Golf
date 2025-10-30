def p(g):
 #Find least frequent nonzero color
 c=sorted({*(l:=sum(g,[]))},key=l.count)[0]
 #Find coordinates of all cell with that color
 return [[c]]
