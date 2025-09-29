# o=lambda l:max(l,key=l.count)
# def p(g):
#     print("")
#     for a in (z:=((0,3,6),(1,4,7))):
#         for b in z:
#             for i in (0,1,2):
#                 for j in (0,1,2):
#                     # print(a[i], b[j], g[a[i]][b[0]::3], [*[*zip(*g)][b[j]]][a[0]::3])
#                     g[a[i]][b[j]]=max(g[a[i]][b[j]],o(g[a[i]][b[0]::3]),o([*[*zip(*g)][b[j]]][a[0]::3]))
#     return g

p=lambda g,z=((0,3,6),(1,4,7)):[[(r:=g[a[i]]).__setitem__(b[j],max(r[b[j]],sorted(r[b[0]::3])[1],sorted([g[x][b[j]]for x in a])[1]))for j in(0,1,2)for b in z]for i in(0,1,2)for a in z]and g