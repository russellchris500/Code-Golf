def p(g):
 h,w=len(g),len(g[0])
 y=[(i,j)for i in range(h)for j in range(w)if g[i][j]==4]
 yr1,yr2,yc1,yc2=min(a[0]for a in y),max(a[0]for a in y),min(a[1]for a in y),max(a[1]for a in y)
 out=[(i,j,g[i][j])for i in range(h)for j in range(w)if g[i][j]not in[0,4]and not(yr1<=i<=yr2 and yc1<=j<=yc2)]
 pr1,pr2,pc1,pc2=min(a[0]for a in out),max(a[0]for a in out),min(a[1]for a in out),max(a[1]for a in out)
 ph,pw=pr2-pr1+1,pc2-pc1+1
 pat=[[0]*pw for _ in range(ph)]
 for i,j,c in out:pat[i-pr1][j-pc1]=c
 ins=[(i-yr1,j-yc1,g[i][j])for i in range(yr1,yr2+1)for j in range(yc1,yc2+1)if g[i][j]not in[0,4]]
 rh,rw=yr2-yr1+1,yc2-yc1+1
 s,or1,oc1=1,0,0
 if ins:
  fi,fj,fc=min(ins)
  for n in range(1,min(rh,rw)):
   if fi+n<rh and fj+n<rw and g[yr1+fi][yc1+fj]==g[yr1+fi+n][yc1+fj]==g[yr1+fi][yc1+fj+n]==g[yr1+fi+n][yc1+fj+n]==fc:
    s=n+1
   else:break
  # Find best alignment by trying all reasonable positions
  best_match=0
  best_or1,best_oc1=0,0
  for trial_or1 in range(rh):
   for trial_oc1 in range(rw):
    matches=sum(1 for i,j,c in ins if 0<=(i-trial_or1)//s<ph and 0<=(j-trial_oc1)//s<pw and pat[(i-trial_or1)//s][(j-trial_oc1)//s]==c)
    if matches>best_match:
     best_match,best_or1,best_oc1=matches,trial_or1,trial_oc1
  or1,oc1=best_or1,best_oc1
 o=[[4 if g[yr1+i][yc1+j]==4 else(pat[(i-or1)//s][(j-oc1)//s]if 0<=(i-or1)//s<ph and 0<=(j-oc1)//s<pw else 0)for j in range(rw)]for i in range(rh)]
 return o