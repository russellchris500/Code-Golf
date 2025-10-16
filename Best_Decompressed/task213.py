p=lambda g,L=len:[g:=[*zip(*[(W:=min(L(r),L(g)))<8<L(r)and[*{*r}-{0,5}]*W or r for r in g if L({*r}-{0,5})>0])]for _ in[0]*4][3]
