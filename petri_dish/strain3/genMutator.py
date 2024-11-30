# genMutator.py
#

import os
import sys



def readFile(fName):

    fileLines = []

    with open(fName, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


def getNewCode():
    codeLines = []

    with open('newCodeFile.txt', 'r') as inFile:
        for line in inFile:
            codeLines.append(line.strip())
    inFile.close()
    return codeLines


def writeNewCode(newCode):

    for l in newCode: # Only write the one line
        if "return" in l:
            f = open('newCodeFile.txt', 'w')
            f.write(l.strip())
            f.close()
    return


def getMutation(dnaFile):
    # Butt ugly but works, ugh

    #print('---------------')
    found = False
    startList = ['#/START']
    endTag = "#/END"
    mutableCode = []

    block = []
    curr = []

    for i in startList:
        for line in dnaFile:
            if found:
                curr.append(line)
                if line.strip().startswith(endTag):
                    found = False
                    #block.append("\n".join(curr))            # Add merged list to final list
                    block.append(curr)
                    curr = []                                # Zero out current list
            else: 
                if line.strip().startswith(i):            # If line starts with start delimiter
                    found = True
                    #curr.append(line.strip())
                    curr.append(line)

    if len(curr) > 0:      # If there are still lines in the current list
        block.append(curr)
    
    #print("block")
    #print(block)
    #print("curr")
    #print(curr)

    for i in block[0]:
        mutableCode.append(i)
    
    #print('---------------')

    return mutableCode


def makeBetter(mutableCode):
    # For now we can easily change math function and/or amount ie. return newNum +,* (any number)
    # So, for now lat's just increase the amount...~?

    newCode = []
    
    for l in mutableCode:
        if "return" in l:
            tmp = l.split("+")
            if len(tmp) == 1: # No "+"
                tmp = l.split("*")
                function = "* "
            else:
                function = "+ "
                
            print("tmp: ", tmp)
            amount = int(tmp[-1])
            print("amount: ", amount)
            amount += 1
            print("amount: ", amount)
            
            newCode.append(tmp[0] + function + str(amount))
        else:
            newCode.append(l)
    
    #print("newCode:")
    #print(newCode)

    return newCode


def mutate(fName):


    if os.path.exists(fName):
        print("FOUND FILE: " , fName)

        """
            The DNA file provided gave good results, so try to enhance it.
            First read code in newCodeFile.txt, and then read DNA file.
            Extract mutation (mutable) code.
            Compare code? Doesn't matter, the DNA file is what worked, so make it better
            Once "better" replace the code in newCodeFile.txt
        """
        print("newCodeFile:")
        newCodeFile = getNewCode()
        print(newCodeFile)
        print('-----')
        print("dnaFile:")
        dnaFile = readFile(fName)
        print(dnaFile)
        print('-----')
        print("mutableCode:")
        mutableCode = getMutation(dnaFile)
        print(mutableCode)
        #for l in mutableCode:
        #    print(l)
        print('-----')
        print("makeBetter:")
        newCode = makeBetter(mutableCode)
        print(newCode)
        print('-----')
        print('replaceCode:')
        writeNewCode(newCode)
        
    else:
        print("{} Not Found!".format(fName))


    return


if __name__ == "__main__":


    print("Start: genMutator: ")
    # For testing using cell1DNA.py

    fName = "cell1DNA.py"

    mutate(fName)

    print("End: genMutator")
        
