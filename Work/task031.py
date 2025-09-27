#p=lambda g:[*zip(*filter(any,zip(*filter(any,g))))]
#p=lambda g,f=filter:[*zip(*f(any,zip(*f(any,g))))]
#p=lambda g:[*filter(any,zip(*filter(any,zip(*g))))]
p=lambda g:[eval("*filter(any,zip("*2+"*g))))")]