from array import *

array1 = array('i', [10,20,30,40,50])
a2 = array('i', [100,200])

for x in array1:
   print(x)

print('---')

array1.insert(-1,60)

for x in array1:
   print(x)

print('---')

array1.append(70)

print(array1)
print('---')

array1.extend(a2)

print(array1)
print('---')

array1.insert(0, -1)
print(array1)
