def p(f,R=range,Z=zip):
 h=[[f[y][x]==0 and all(not(0<=y+dy<30 and 0<=x+dx<30) or f[y+dy][x+dx]==0 for dy in(-1,0,1) for dx in(-1,0,1) if dy|dx) for x in R(30)]for y in R(30)]
 H=[0]*30;A=[]
 for y in R(30):
  for x in R(30):H[x]=H[x]+1 if h[y][x] else 0
  for L in R(30):
   k=H[L]
   if k:
    for r in R(L,30):
     if not H[r]:break
     k=min(k,H[r]);[A.append((y-i+1,L,y,r,(r-L+1)*i))for i in R(1,k+1)]
 if not A:return [r[:]for r in f]
 w=lambda e:e[3]-e[1]+1;h=lambda e:e[2]-e[0]+1
 A.sort(key=lambda t:(-t[4],t[0],t[1]))
 J=next((q for q in A if w(q)>h(q)),0);P=next((q for q in A if h(q)>w(q)),0)
 I=J and P and (J if w(J)>h(P) else P if w(J)<h(P) else (J if J[4]>=P[4] else P)) or J or P or A[0]
 s=[r[:]for r in f]
 U=lambda e:[s[y].__setitem__(slice(e[1],e[3]+1),[3]*w(e))for y in R(e[0],e[2]+1)]
 O=lambda a,b:a[1]<=b[3]and b[1]<=a[3]and a[0]<=b[2]and b[0]<=a[2]
 V='vh'[w(I)<=h(I)]
 N=lambda e:(e[1]==0 or e[3]==29) if V=='h' else (e[0]==0 or e[2]==29)
 C=lambda e:(all(0<=y<30 and 3 not in s[y][e[1]:e[3]+1] for y in(e[0]-1,e[2]+1)) if V=='h'
            else all(0<=x<30 and 3 not in [*Z(*s[e[0]:e[2]+1])][x] for x in(e[1]-1,e[3]+1)))
 B=lambda e:((e[3]+1==I[1]or e[1]-1==I[3])and e[0]<=I[2]and e[2]>=I[0]) if V=='h' else ((e[2]+1==I[0]or e[0]-1==I[2])and e[1]<=I[3]and e[3]>=I[1])
 U(I);Rr=[I]
 while 1:
  for z in sorted(A,key=lambda t:(not N(t),-t[4],t[0],t[1])):
   if (w,h)[V>'h'](z)<5 or not C(z) or not B(z) or any(O(z,q)for q in Rr):continue
   U(z);Rr+=[z];break
  else:break
 return s