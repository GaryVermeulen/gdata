import os
from pathlib import Path
from simpJ import readJSON


def readKB():

    inLines = []
    kbFile   = 'simpXnew.py'
    progPath = os.getcwd()

    inFile = Path(progPath + '/' + kbFile)
    f = open(inFile, 'r')

    for line in f:
        l = line.rstrip()
#        print(l)
        inLines.append(l)
    f.close()

    return inLines


def findSuperClass(line, superclass):

    sClass = None
    lineLst = line.split()

    if lineLst[0] == 'class':
        i = lineLst[1].find(superclass)
        if i == 0:
            sub = lineLst[1].split('(')
            if sub[1] != "ThingMaker):":
                sClass = sub[0]
    
    return sClass


def findParallelClass(line, superClass): # Insert new class below

    pClass = None
    lineLst = line.split()
    insertLine = 0

    print('- - - - -')
    print(superClass)
    print(lineLst)
    

    if lineLst[1] == 'class':
        i = lineLst[2].find(superClass)
        if i > 0:
            print(lineLst[2])
            print(i)
            ln = lineLst[0].replace(':', '')
            print('ln: ', ln)
            insertLine = int(ln) + 6
            print('line to insert: ', insertLine)

        
    print('- - - - -')
    print(insertLine)
    print('- - - - -')
    return insertLine


def checkClass(kb):

    classThingsFound = []

    lineNum = 0

    for x in kb:
        lineNum += 1
        y = x.find(searchClass) 
        if  y > -1:
            tmp = str(lineNum) + ': ' + x
            classThingsFound.append(tmp)

    return classThingsFound


def checkSuperClass(kb):

    lineNum = 0
    lineInsertPoint = 0
    
    # look for superclass or parallel, do any exist?    
    for x in kb:
        lineNum += 1
        y = x.find(searchSuperClass)
        if y > -1:
            tmp = str(lineNum) + ': ' + x
            superClassThingsFound.append(tmp)
            s = findSuperClass(x, searchSuperClass)
            if s != None:
                sClass = s
            lip = findParallelClass(tmp, searchSuperClass)
            if lip != 0:
                lineInsertPoint = lip
                
    return sClass, lineInsertPoint

    


if __name__ == "__main__":

    name = 'car'
    superclass = 'vehicle'
    canDo = list('transport')

    searchClass = name + superclass.capitalize()
    searchSuperClass = superclass.capitalize()

    foundLine = ''
    lineNum = 0
    lineInsertPoint = 0

#    classThingsFound = []
    superClassThingsFound = []
    sClass = None

    d = readJSON()

#    print(d)

    for x in d: v = x 

#    for y in v:
#        print(y)
#        print(' ', y.keys())
#        print(' ', y.values())
#
#    print('---')

    orgKB = readKB()

    classThingsFound = checkClass(orgKB)

    sClass, lineInsertPoint = checkSuperClass(orgKB)

    
    print(searchClass)
    if len(classThingsFound) == 0:
        print('{} Not Found'.format(searchClass))
    else:
        for i in classThingsFound: print(i)
    print('------------')
    print(searchSuperClass)
    if len(searchSuperClass) == 0:
        print('{} Not Found'.format(searchSuperClass))
    else:
        for i in superClassThingsFound: print(i)
    print('------------')
    print('superclass: ', sClass)
    print('lineInsertPoint: ', lineInsertPoint)
