def p(a,R=range):
 h,w=len(a),len(a[0])
 for y in R(h):
  for x in R(w):
   if a[y][x]:continue
   H=W=1
   while y+H<h and all(a[y+H][x+i]==0for i in R(W)):H+=1
   while x+W<w and all(a[y+i][x+W]==0for i in R(H)):W+=1
   P=set()
   if y:P|={(y-1,x+i)for i in R(-1if x else 0,W+(x+W<w))}
   if y+H<h:P|={(y+H,x+i)for i in R(-1if x else 0,W+(x+W<w))}
   if x:P|={(y+i,x-1)for i in R(H)}
   if x+W<w:P|={(y+i,x+W)for i in R(H)}
   if P and all(a[i][j]==5for i,j in P)and not any(0<=i<h and 0<=j<w and a[i][j]==5and(i,j)not in P
     for Y,X in((y-1,x-1),(y-1,x+W),(y+H,x-1),(y+H,x+W))
     for i,j in((Y+1,X),(Y-1,X),(Y,X+1),(Y,X-1))):
    for i in R(H):
     for j in R(W):a[y+i][x+j]=4
 return a
