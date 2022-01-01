#!/usr/bin/env python3
#
# One-way functions...
#

import math


p = 2 # 48611
q = 4 # 53993
x = p * q
n = 10 # 7

def f(x):
    x2 = x * x
    return x2

def fi(fx, n):
    xd = 0
    xm = 0
    if n != 0:
        xd = fx / n
        xm = fx % n
    print("xd: " + str(xd))
    print("xm: " + str(xm))
    
print("P: " + str(p))
print("q: " + str(q))
print("x: " + str(x))
print("n: " + str(n))
print("---------------")
    
fx = f(x)    
    
print("f(x): " + str(fx))
print("---------------")    

#for n in range(2):   
#    fy = fi(fx, n)    
#    print("fy: " + str(fy))
  
fi(fx, 2)

print("SQRT: " + str(math.sqrt(fx)))
    
print("FINI")    
