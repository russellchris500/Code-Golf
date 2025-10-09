<<<<<<< HEAD
def p(i):
 n=next((e for e in i if 0not in e),None)
 if not n:return i
 e=[];[e.append(t)for t in n if t not in e]
 for(f,d)in enumerate(i):
  if 0in d and any(d):
   t=[];[t.append(e)for e in d if e not in t and e]
   if len(e)==len(t):d={**zip(e,t)};i[f]=[d[e]for e in n]
 return i
=======
p=lambda g:[[*map(dict([*zip(g[1],r)][::-1]).get,g[1])]for r in g]
>>>>>>> 1db8808c6de37a311823ae49eb67bda6d9ff326c
