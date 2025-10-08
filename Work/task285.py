#or, if you need all 4 of them in one script:
r=lambda a:(o:=[r+r[::-1]for r in a])+o[::-1]   # UL
R=lambda a:[r[::-1]for r in a]                  # horizontal flip

r_ul=r
r_ur=lambda a:r(R(a))[::-1]                     # UR
r_ll=lambda a:r(a[::-1])[::-1]                  # LL
r_lr=lambda a:R(r(R(a)[::-1]))[::-1]            # LR (fixed)


# a=[[0,0,0,0],[0,6,0,0],[0,8,4,4],[0,0,4,4]]
a=[[1,2],[3,4]]

print("reflected from upper left:")
for row in r_ul(a):
    print(row)
print()
print("reflected from upper right:")
for row in r_ur(a):
    print(row)
print()
print("reflected from lower left:")
for row in r_ll(a):
    print(row)
print()
print("reflected from lower right:")
for row in r_lr(a):
    print(row)