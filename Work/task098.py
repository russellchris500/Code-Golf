import re
p=lambda g:eval(re.sub('(?<=%s, )[^0](?=, %s)'%(s:='[^0].{%d}[^0]'%(len(g[0])*3+1),s),'0',str(g)))
#p=lambda g:eval(re.sub('(?<=[^0].{%d}[^0], )[^0](?=, [^0].{%d}[^0])'%(n:=len(g[0])*3+1,n),'0',str(g)))