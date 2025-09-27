# Original code:
# b=lambda g:max(sum(map(any,g)),sum(map(any,zip(*g))))%2 # returns 1 if figure width/height is odd, 0 if even
# a=lambda g:[*zip(*(g+[10*[0]]*b(g))[::-1])] #Adds a line at the top if odd size, then flips
# p=lambda g:[[l or r*2 for l,r in zip(x,y)]for x,y in zip(g,a(g))] # rotates 90 degrees then overlays
p=lambda g:[[l or r*2for l,r in zip(x,y)]for x,y in zip(g,[*zip(*((g+[10*[0]]*(max(sum(map(any,g)),sum(map(any,zip(*g))))%2))[::-1]))])]