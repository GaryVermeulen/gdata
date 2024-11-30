# alGen1.py
#
# Algorithm-generator
#
"""
 Guidelines:
  (i)   Selecting good solutions from a solution base,
  (ii)  Generating new solutions using the selected solutions,
  (iii) Choosing inferior or spurious solutions for replacement,
  (iv)  Updating the solution base with good new or old solutions.

 Goal:
  Generate a list of prime numbers
  
"""

import os
import pickle


def readDNAFile(fName):

    fileLines = []

    with open(fName, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


def isNumPrime1(num):
    #print("isNumPrime1: num: ", num)
    retValue = False
    # Negative numbers, 0 and 1 are not primes
    if num > 1:
        # Iterate from 2 to n // 2
        for i in range(2, (num//2)+1):
            # If num is divisible by any number between
            # 2 and n / 2, it is not prime
            if (num % i) == 0:
                #print(num, "is not a prime number")
                break
        else:
            #print(num, "is a prime number")
            retValue = True
    else:
        print(num, "is not <=1 and is not prime number")

    return retValue




def getMutableCode(dnaFile):
    # Butt ugly but works, ugh

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
                    block.append(curr)
                    curr = []                                # Zero out current list
            else:
                if line.strip().startswith(i):            # If line starts with start delimiter
                    found = True
                    curr.append(line)

    if len(curr) > 0:      # If there are still lines in the current list
        block.append(curr)

    for i in block[0]:
        mutableCode.append(i)

    return mutableCode


def createStarterSB(logsFile, solutionBaseFile):

    sb = []
    logs = pickle.load(open(logsFile, 'rb'))
    
    for log in logs:
        
        totTrue = 0
        lineCnt = 0
        for line in log[1]:
            lineCnt += 1

            if line[-1] == 'True':
                totTrue += 1
        P = (totTrue / lineCnt) * 100
        # Extract formula (code) from DNA file
        dnaFile = line[2]
        dnaFileList = readDNAFile(dnaFile)
        mutableCode = getMutableCode(dnaFileList)

        # Since this is a "starter" save all data
        sb.append(str(round(P)) + ',' + str(lineCnt) + ',' + str(totTrue) + ',' +  mutableCode[1])
    
    print('Saving starter solution base to pickle...')
    with open(solutionBaseFile, "wb") as f:
        pickle.dump(sb, f)
    f.close()
        
    print('Pickle saved.')

    return sb


def generateNewSolution(sb):
    
    newSolution = []

    # Sort play...
    sb.sort(reverse=True)

    for s in sb:
        print(s)

    bestOption = sb[0]
    print(bestOption)

    # Extract code
    bOptLst = bestOption.split(',')
    print(bOptLst)

    codeLst = bOptLst[-1].split('return')
    code = codeLst[-1].strip()
    print(code)

    if '+' in code:
        cLst = code.split('+')
        function = '+'

    print(cLst)
    for c in cLst:
        tstChar = c.strip() 
        if tstChar.isnumeric():
            print("numeric: ", tstChar)
            numVar = tstChar
        elif tstChar.isalpha():
            print("alpha: ", tstChar)
            alphaVar = tstChar
        else:
            print("unknown: ", tstChar)

    print('====')
    trueCount = 0
    for i in range(0, 100):
        #print('i:', i)
        ans = i + int(numVar)
        #print(ans)
        retVal = isNumPrime1(ans)
        if retVal:
            #print('retVal: ', retVal)
            trueCount += 1
        #print('---')
    print('trueCount: ', trueCount)
    P = (trueCount/100) * 100
    print('P: ', round(P))
    print('----')
        

    #ans = eval(code)
    #print(ans)

    # Make a test run from 0 to 10
    
        

    return newSolution


if __name__ == "__main__":

    solutionBaseFile = "solutionBase.p"
    logsFile = "logs.p"
    

    # (i) -- Before we can select from we must
    # build a starter SB
    if os.path.exists(solutionBaseFile):
        print("Solution Base File Found: " , solutionBaseFile)
        sb = pickle.load(open(solutionBaseFile, 'rb'))


    else:
        print("Solution Base File NOT Found: " , solutionBaseFile)
        if os.path.exists(logsFile):
            print("Creating starter SB from: ", logsFile)
            sb = createStarterSB(logsFile, solutionBaseFile)
        else:
            print("Logs File NOT Found: " , logsFile)

    print('Raw sb:')
    for s in sb:
        print(s)
    print('-----')

    # (ii) -- This is going to be interesting
    newSolution = generateNewSolution(sb)
    
    
