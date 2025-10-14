def p(f,x=range):
 N=30
 h=[[not f[i][z]and all(not(0<=i+l<N and 0<=z+a<N)or not f[i+l][z+a]for l in(-1,0,1)for a in(-1,0,1)if l|a)for z in x(N)]for i in x(N)];p=[0]*N;a=[]
 for y in x(N):
  for b in x(N):p[b]=h[y][b]and p[b]+1
  for M in x(N):
   l=p[M]
   if l:
    for z in x(M,N):
     if not p[z]:break
     l=min(l,p[z]);[a.append((y-i+1,M,y,z,(z-M+1)*i))for i in x(1,l+1)]
 if not a:return[[*i]for i in f]
 t,e=lambda g:g[3]-g[1]+1,lambda g:g[2]-g[0]+1;a.sort(key=lambda t:(-t[4],t[0],t[1]))
 j=next((i for i in a if t(i)>e(i)),0);p=next((i for i in a if e(i)>t(i)),0)
 i=j and p and(j if t(j)>e(p)else p if t(j)<e(p)else j if j[4]>=p[4]else p)or j or p or a[0];s=[[*i]for i in f]
 def u(e):
  for r in x(e[0],e[2]+1):s[r][e[1]:e[3]+1]=[3]*t(e)
 H=lambda e,i:e[1]<=i[3]and i[1]<=e[3]and e[0]<=i[2]and i[0]<=e[2];l='vh'[t(i)<=e(i)]
 n=lambda e:e[1]==0 or e[3]==N-1 if l=='h'else e[0]==0 or e[2]==N-1
 b=lambda e:(e[3]+1==i[1]or e[1]-1==i[3])and e[0]<=i[2]and e[2]>=i[0]if l=='h'else(e[2]+1==i[0]or e[0]-1==i[2])and e[1]<=i[3]and e[3]>=i[1]
 c=lambda e:all(not(0<=r<N and 3 in s[r][e[1]:e[3]+1])for r in(e[0]-1,e[2]+1))if l=='h'else all(not(0<=c<N and any(s[y][c]==3 for y in x(e[0],e[2]+1)))for c in(e[1]-1,e[3]+1))
 u(i);r=[i]
 S=sorted(a,key=lambda t:(-n(t),-t[4],t[0],t[1]))
 while 1:
  for z in S:
   if(t,e)[l>'h'](z)<5 or not c(z) or not b(z) or any(H(z,q)for q in r):continue
   u(z);r+=[z];break
  else:break
 return s