def p(g):
 h,w=len(g),len(g[0])
 o=[r[:]for r in g]
 c={}
 for r in g:
  for x in r:c[x]=c.get(x,0)+1
 oc=min([x for x in c if x!=0],key=c.get)
 for i in range(h):
  for j in range(w):
   if g[i][j]==oc:
    for rh in range(2,h-i+1):
     for rw in range(2,w-j+1):
      if i+rh<=h and j+rw<=w:
       if all(g[i][x]==oc and g[i+rh-1][x]==oc for x in range(j,j+rw))and all(g[y][j]==oc and g[y][j+rw-1]==oc for y in range(i,i+rh))and all(g[y][x]==0 for y in range(i+1,i+rh-1)for x in range(j+1,j+rw-1)):
        ih,iw=rh-2,rw-2
        for ii in range(h-ih+1):
         for jj in range(w-iw+1):
          if all(g[y][x]==0 for y in range(ii,ii+ih)for x in range(jj,jj+iw))and not(ii>=i and ii+ih<=i+rh and jj>=j and jj+iw<=j+rw):
           for y in range(ii-1,ii+ih+1):
            for x in range(jj-1,jj+iw+1):
             if 0<=y<h and 0<=x<w and(y==ii-1 or y==ii+ih or x==jj-1 or x==jj+iw):o[y][x]=oc
           return o
 return o