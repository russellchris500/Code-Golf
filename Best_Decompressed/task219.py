def p(g):
 t=[];b=1;s=[];R=range
 for r in R(15):
  if any(g[r])&b:t+=[r]
  elif t:b=0
  s+=[{i for i in R(10)if g[r][i]}]
 L=len(t)
 for r in R(15-L):
  for c in R(-(s[1]=={0,1,2,3}),8):
   a=set();b=set();z=0
   for i in R(L):o={i+c for i in s[t[i]]};b|=s[r+i]^o;a|=s[r+i];z+=len(s[r+i]&o)>0
   if(max({-2}|a&b)<c)*z*(s[r-1]|s[r+L]<{1}):[g[r+i].__setitem__(j+c,1)for i in R(L)for j in s[t[i]]if-1<j+c<10and{j+c}-s[r+i]];break
 return g
