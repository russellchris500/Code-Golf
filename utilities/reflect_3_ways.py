#This code reflects a list of lists, a, 3 times - horizontally, vertically, and both.

#if for some upstream reason, you need to flatten the list first, this will work. This function flattens the list for you, reflects 3 ways, then unflattens
def reflect_4fold_with_flattening(a):
 f=[x for r in a for x in r];w=len(a[0]);o=[]
 for i in range(len(a)):
  n=f[i*w:i*w+w]
  o+=n+n[::-1]
 o+=o[::-1]
 return [o[i:i+2*w] for i in range(0, len(o), 2*w)]

#if you don't need to flatten for any reason:
def reflect_4fold_without_flattening(a):
 o=[r+r[::-1]for r in a]
 return o+o[::-1]