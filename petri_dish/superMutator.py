# superMutator.py
#

import os
import sys

def readFile(fName):

#    inFile = open(fName, "r")
#    inLines = inFile.read()
#    inFile.close()
#
#    return inLines

    fileLines = []

    with open(fName, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines

def writeFile(fName, ): # Replace code in fName @ line after #P!
    newFile = []

    print("fName: ", fName)

    file = readFile(fName)
    for line in file:
        print(line)
    print('---------------')

    newCode = getNewCode(fName)

    for line in newCode:
        print(line)
    print('---------------')

    
    found = False

    for i in range(len(file)):

        if file[i].strip() == "#P!":
            print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append("    " + j)
            found = True
        else:
            print("NF: ", file[i])
            if found:
                found = False
                continue
            newFile.append(file[i])
    
            
    print('---------------')
        

    for l in newFile:
        print(l)

#    outFile = open(fName, "w")
#    outFile.writelines(newFile)
#    outFile.close()

    with open(fName, "w") as outFile:
        for l in newFile:
            outFile.write(l + "\n")
    outFile.close()


    return

def getNewCode(fName):
    codeLines = []

    with open('newCodeFile.txt', 'r') as inFile:
        for line in inFile:
            codeLines.append(line.strip())
    inFile.close()
    return codeLines    

if __name__ == "__main__":

    #myInput = readFile()

    print("Super Mutator: ")

    fName = input("Enter cell filename to mutate CR to exit: ")

    if fName == "":
        sys.exit("Exiting without change.")
    else:
        if os.path.exists(fName):
            print("FOUND: " , fName)
            print("Replacing code @ #P!")
            writeFile(fName)
            
        else:
            print("{} Not Found!".format(fName))
    
    print(".End.")
        
