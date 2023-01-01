#
# modMod.py modify a module to then reload the modifed module
#
import os

# module to modify
inFile = '/home/gary/src/p/reload/myMod1.py'
buFile = '/home/gary/src/p/reload/myMod1.py.txt'

# make a backup copy
os.system('cp ' + inFile + ' ' + buFile)

def lIndent(l):

    indent = ''

    spaces = len(l) - len(l.lstrip())

    for s in range(0, spaces):
        indent = indent + ' '

    return indent

inLines = []
newLines = []
lineCount = 0

thingMissing = 'Bob'

print('-----')

# read file
#with open(inFile, 'r') as f:
            #while (line := f.readline().rstrip()):

f = open(inFile, 'r')

for line in f:

    l = line.rstrip()
    print(l)
    inLines.append(l)

f.close()

print('-----')
print(inLines)
print('-----')

for l in inLines:
    lineCount += 1
    print('{}: {}'.format(lineCount, l))

    if 'else:' in l:
        print("Found else at ", lineCount)
        insertPoint = lineCount

print('insertPoint: ', insertPoint)

lineCount = 0
for l in inLines:
    lineCount += 1
    if lineCount < insertPoint:
        newLines.append(l)
    elif lineCount == insertPoint:
        indent = lIndent(l)
        newLines.append(indent + 'elif i == "' + thingMissing + '":')
        newLines.append(indent + indent + "o = 'myFun1 output with ' + str(i) + ' and ' + str(myFun1Var)")
        newLines.append(l)
    else:
        newLines.append(l)

    
print(newLines)


# write to file
with open(inFile, 'w') as f:
    for l in newLines:
        f.write("%s\n" % l)

print('\nDone')

