from collections import*
def p(i):
 t=Counter(v for v in sum(i,[])if v).most_common()[-1][0]
 a=b=l=r=-1
 for y,row in enumerate(i):
  for x,v in enumerate(row):
   if v==t:
    a=y if a<0 else a;b=y;l=x if l<0 or x<l else l;r=max(r,x)
 return[i[y][l:r+1]for y in range(a,b+1)]