def p(j):
 a=sum(j,[]).index(2);c,e=divmod(a,5);j[c][e]=0
 if c*e:j[c-1][e-1]=3
 if c<2and e:j[c+1][e-1]=8
 if e<4and c:j[c-1][e+1]=6
 if c<2and e<4:j[c+1][e+1]=7
 return j
