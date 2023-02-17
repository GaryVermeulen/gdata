# Adds a new class to simpKB.py
# In an effort to dynamically update KB
#

import os
import sys


kbFile   = 'simpKB.py'
kbBU = 'simpKB.py.bu'
superClassThingsFound = []


def readKB():

    inLines = []
    global kbFile
    progPath = os.getcwd()
    inFile = progPath + '/kb/' + kbFile
    
    f = open(inFile, 'r')

    for line in f:
        l = line.rstrip()
#        print(l)
        inLines.append(l)
    f.close()

    return inLines


def writeKB(newKB):

    global kbFile
    progPath = os.getcwd()
    outFile = progPath + '/kb/' + kbFile
    buFile = progPath + '/kb/' + kbFile + '.bu'

    os.system('cp ' + outFile + ' ' + buFile)
    
    with open(outFile, 'w') as f:
        for l in newKB:
            f.write("%s\n" % l)
            print(l)
    f.close()

    return None


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

    if lineLst[1] == 'class':
        i = lineLst[2].find(superClass)
        if i > 0:
            ln = lineLst[0].replace(':', '')
            insertLine = int(ln) + 6

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
    sClass = ''
    
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


def createNewClass(name, sClass):

    nc = []
    indent = '    '

    nc.append('class ' + name + sClass + '(' + sClass + '):')
    nc.append(indent + 'def __int__(self):')
    nc.append(indent + indent + 'super().__init__()')
    nc.append(indent + indent + 'self.name = "' + name + sClass + ' name"')
    nc.append(indent + indent + 'self.classInfo = "' + name + sClass + ' class info"')
    nc.append('')
    
    return nc


def insertNewClass(orgKB, newClass, lineInsertPoint):

    lineNum = 0
    indent = '    '
    lines2Add = len(newClass)

    while lines2Add > 0:
        orgKB.insert(lineInsertPoint + lineNum, newClass[lineNum])
        lineNum += 1
        lines2Add -= 1
                
    return orgKB


def add2Factory(newKB, name, sClass):

    lineNum = 0
    indent = '    '
    line2Insert = ''
    foundStartLine = False
    foundStartBracket = False
    foundEndBracket = False
    startBrkNum = 0
    endBrkNum = 0
    searchClass = sClass.capitalize()
#    print('add2Factory: ', searchClass)
    line2Search = 'class ' + searchClass + '(ThingMaker):'
#    print('looking for: ', line2Search)

    for i in newKB:
        lineNum += 1
        if i == line2Search:
#            print('FOUND: {}  At: {}'.format(i, lineNum))
            foundStartLine = True
        if foundStartLine and (i.find('{') != -1):
#            print('FOUND START Brk: {}  At: {}'.format(i, lineNum))
            startBrkNum = lineNum
            foundStartBracket = True
        if foundStartLine and foundStartBracket and (i.find('}') != -1):
#            print('FOUND END Brk: {}  At: {}'.format(i, lineNum))
            endBrkNum = lineNum
            foundEndBracket = True
        if foundEndBracket:
            break
    line2Insert = indent + indent + indent + '"' + name + '": ' + name + searchClass + 'Thing(),'
#    print('add2Factory: ', line2Insert)
    newKB.insert(startBrkNum, line2Insert)

    return newKB


#def addNewClass: What was I going to add?




    

if __name__ == "__main__":

    # Simple new input sample
    name = 'car'
    superclass = 'vehicle'
    canDo = list('transport')

    searchClass = name + superclass.capitalize()
    searchSuperClass = superclass.capitalize()

    print('=======================================')

    print('Sample input:')
    print('name:', name)
    print('searchClass: ', searchClass)
    print('searchSuperClass: ', searchSuperClass)
    print('------------')

    foundLine = ''
    lineNum = 0
    lineInsertPoint = 0

    sClass = None


    orgKB = readKB()

    print('orgKB:')
    for i in orgKB: print(i)
    print('------------')

#    sys.exit("Stopping after readKB")

    classThingsFound = checkClass(orgKB)

    if len(classThingsFound) < 1:
        print('No classThingsFound')
        print('{} Not Found'.format(searchClass))
    else:
        print('classThingsFound:')
        for i in classThingsFound: print(i)
        sys.exit('Class Found, Exiting...')
        
    print('------------')
 
    

    sClass, lineInsertPoint = checkSuperClass(orgKB)

    print('sClass: ', sClass)
    print('lineInsertPoint: ', lineInsertPoint)

    if len(superClassThingsFound) < 1:
        print('{} Not Found'.format(searchSuperClass))
    else:
        for i in superClassThingsFound: print(i)
        
    print('------------')

    
    newClass = createNewClass(name, sClass)

    print('newClass: ')
    for i in newClass: print(i)
    
    print('------------')
    
    newKB = insertNewClass(orgKB, newClass, lineInsertPoint)

    print('newKB 1st return len: ', len(newKB))
    lineNum = 0
    for i in newKB:
        lineNum += 1
        print(str(lineNum) + ': ' + i)

    print('------------')


    newKB = add2Factory(newKB, name, superclass)

    print('newKB 2nd return len: ', len(newKB))
    lineNum = 0
    for i in newKB:
        lineNum += 1
        print(str(lineNum) + ': ' + i)

    print('------------')


    writeKB(newKB)

    print('End.')

    
