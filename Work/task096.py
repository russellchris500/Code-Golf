import re
def p(g,R=range,f=re.findall):
 t=re.sub(', ','',str(g+[*zip(*g)]));t+=t[::-1];b=int(max(t,key=t.count));B={0:(0,b)}
 for c in{*R(10)}-{b}:
  if v:=f(f'{c}+',t):m=len((f(f'{c}{c}[^]){c}]+{c}',t)+['000'])[0])-3;B[len(max(v,key=len))*(2-(m<1))+m>>1]=-~m>>1,c
 x=2*max(B)+1;return[[b if z[0]<(q:=B[z[1]])[0]else q[1]for j in R(x)if(z:=sorted([abs(j-x//2),abs(i-x//2)]))]for i in R(x)]