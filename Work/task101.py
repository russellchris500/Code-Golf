def p(g):
 h,w=len(g),len(g[0])
 b=[(i,j)for i in range(h)for j in range(w)if g[i][j]==1]
 r=[(i,j)for i in range(h)for j in range(w)if g[i][j]==2]
 tr=[p for p in r if any(abs(p[0]-q[0])+abs(p[1]-q[1])==1 for q in b)]
 ir=[p for p in r if p not in tr]
 if not(tr and ir and b):return g
 def bb(l):return min(p[0]for p in l),max(p[0]for p in l),min(p[1]for p in l),max(p[1]for p in l)
 tri,trx,trj,try_=bb(tr)
 iri,irx,irj,iry=bb(ir)
 bri,brx,brj,bry=bb(b)
 tci,tcj=(tri+trx)//2,(trj+try_)//2
 ici,icj=(iri+irx)//2,(irj+iry)//2
 bci,bcj=(bri+brx)//2,(brj+bry)//2
 tw,th=try_-trj+1,trx-tri+1
 iw,ih=iry-irj+1,irx-iri+1
 s=min(iw//tw,ih//th)if tw and th else 1
 for bi,bj in b:
  di,dj=bi-bci,bj-bcj
  ni,nj=ici+di*s,icj+dj*s
  if 0<=ni<h and 0<=nj<w and g[ni][nj]!=2:g[ni][nj]=1
 return g