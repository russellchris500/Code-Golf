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

r=lambda a:(o:=[r+r[::-1]for r in a])+o[::-1]

a = [[1,2],[3,4]]
# print(reflect_4fold_without_flattening(a))

#reflect from starting point of all 4 different quadrants:
a=[[1,2],
   [3,4]]

r=lambda a:(o:=[r+r[::-1]for r in a])+o[::-1]
r_ur=lambda a:r([r[::-1]for r in a])[::-1]
r_ll=lambda a:r(a[::-1])[::-1]
r_lr=lambda a:[r[::-1]for r in r([r[::-1]for r in a][::-1])][::-1]

print("reflected from upper left:")
for row in r(a):
 print(row)
print("reflected from upper right:")
for row in r_ur(a):
 print(row)
print("reflected from lower left:")
for row in r_ll(a):
 print(row)
print("reflected from lower right:")
for row in r_lr(a):
 print(row)

#or, if you need all 4 of them in one script:
r=lambda a:(o:=[r+r[::-1]for r in a])+o[::-1]
R=lambda a:[r[::-1]for r in a]

r_ul=r
r_ur=lambda a:r(R(a))[::-1]
r_ll=lambda a:r(a[::-1])[::-1]
r_lr=lambda a:R(r(R(a)[::-1]))[::-1] 

a=[[1,2],[3,4]]
print("reflected from upper left:")
for row in r(a):
 print(row)
print("reflected from upper right:")
for row in r_ur(a):
 print(row)
print("reflected from lower left:")
for row in r_ll(a):
 print(row)
print("reflected from lower right:")
for row in r_lr(a):
 print(row)