#p=lambda g:[*zip(*filter(any,zip(*filter(any,g))))]
#p=lambda g,f=filter:[*zip(*f(any,zip(*f(any,g))))]
#p=lambda g:[*filter(any,zip(*filter(any,zip(*g))))]
# p=lambda g:[eval("*filter(any,zip("*2+"*g))))")]
#p=lambda g,c=2:[r for r in g if any(r)]
p=lambda g:[*zip(*filter(any,zip(*filter(any,g))))]
p=lambda g,c=60:c>0and p([*zip(*g[::-1])],c-1)or g