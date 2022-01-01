#!/usr/bin/env python3
#
# simple DFA it determine if w has 1 or 3 0's in it...
#

w = '0111ab0c110'

count = 0

for c in w:
    if c == '0':
        count += 1

if count == 1 or count == 3:
    print("Accept: count = " + str(count))
else:
    print("Reject: count = " + str(count))
    
    
