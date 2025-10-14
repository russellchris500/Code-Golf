# If the row and prev (modifed)row are equal then each p is p^a, where a is the prev pixel
p=lambda g,a=[0]:[a:=(a==r and[...for p in r]or r)for r in g]