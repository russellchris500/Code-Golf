def p(s,R=range):
 h,w=len(s),len(s[0]);n=0;t=[]
 for r in R(h):
  for c in R(w):
   if s[r][c]and n==0:n=s[r][c]
   if s[r][c]==n and n:t.append([r,c])
 T,L=t[0];B,W=t[-1];s=s[T+1:B];s=[g[L+1:W]for g in s]
 for r in R(len(s)):
  for c in R(len(s[0])):
   if s[r][c]>0:s[r][c]=n
 return s