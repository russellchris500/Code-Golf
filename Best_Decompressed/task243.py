p=lambda g,l=80:l and p([[a|(a:=p)==1or p for p in r]for r in zip(*g[::-1])if(a:=2)],l-1)or g
