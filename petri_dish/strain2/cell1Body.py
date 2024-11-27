# cell1Body.py
#
# "Evolved" from cellAdd.py
#

import os
import sys
import time
import shutil
import random
import importlib
from subprocess import call


pid = os.getpid()
ppid = 0

def writeLog(outNum):

    whoami = __file__
    baseStr = whoami[:-3] # remove the .py
    newStr = baseStr + ".log"
    outFile = open(newStr, "a")
    outFile.writelines(str(outNum))
    outFile.close()

    return


def readDNAFile(fName):

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


def getLastFile():

    # Read file
    fLst = []
    with open("fileList.txt", "r") as f:
        for line in f:
            line = line.replace("\n", "")
            lineLst = line.split(',')
            fLst.append(lineLst)
    f.close()

    # Get last entry
    ppid = fLst[-1][0]
    lastFile = fLst[-1][1]
    lastDNA = fLst[-1][2]

    return ppid, lastFile, lastDNA


def setNextFile(lastFile, lastDNA):
    
    # Extract the number from the file name
    bx = [i for i in range(len(lastFile)) if lastFile.startswith("B", i)]
    bIdx = bx[0]
    cIdx = 0

    head = lastFile[:4] # pick off cell
    tail = lastFile[-7:] # pick off Body.py
        
    num = lastFile[cIdx + 4:bIdx]

    nextNum = int(num) + 1

    # Next file names
    newFile = head + str(nextNum) + tail
    newDNA = head + str(nextNum) + "DNA.py"

    # Append to file
    fileEntry = str(pid) + "," + newFile + "," + newDNA + "\n"

    filer = open("fileList.txt", "a")
    filer.writelines(fileEntry)
    filer.close()
    
    return newFile, newDNA


def mutateDNAFile(newDNA):

    file = readDNAFile(newDNA)

    newCode = getNewCode()

    found = False
    newFile = []
    for i in range(len(file)):
        if file[i].strip() == "#P!":
            #print("FOUND: ", file[i])
            newFile.append(file[i])
            for j in newCode:
                newFile.append("    " + j)
            found = True
        else:
            #print("NF: ", file[i])
            if found:
                found = False
                continue
            newFile.append(file[i])

    with open(newDNA, "w") as outFile:
        for l in newFile:
            outFile.write(l + "\n")
    outFile.close()

    return


def replicate(ppid, dnaFile, num):
    print("-----")
    print("replicate:")

    ppid, lastFile, lastDNA = getLastFile()
    newFile, newDNA = setNextFile(lastFile, lastDNA)
        
    # Create file (replicant)
    shutil.copyfile(lastFile, newFile)

    # Create matching DNA file
    shutil.copyfile(lastDNA, newDNA)

    # Mutate DNA?
    random_int = random.randint(0, 1) # Not sure how we want to do this...~? 50/50?
    if random_int == 1:
        # Mutate
        print("*** Mutating: ", newDNA)
        mutateDNAFile(newDNA)
    else:
        print("No mutation.")
    
    print("Starting replicated file: ", newFile)
    print("Replicated DNA file: ", newDNA)

    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newFile + "; bash"
    call(callStr)
    
    return


if __name__ == "__main__":

    MAXPOP = 50
    whoami = __file__

    currentNum = 0
    loopCnt = 1

    basePath = "/home/gary/src/petri_dish/strain2"
    
    start_time = time.time()
    end_time = start_time + 120  # 2 minutes

    print("--- START CELL INSTANCE ---")
    print("whoami: ", whoami)
    print("basePath: ", basePath)

    # Determine and import appropriate DNA module
    #
    if "cell1Body.py" in whoami: # First cell -- rewrite file
        dnaFile = "cell1DNA.py"
        dnaModule = "cell1DNA"

        fileEntry = str(pid) + ",cell1Body.py," + dnaFile + "\n"

        filer = open("fileList.txt", "w")
        filer.writelines(str(fileEntry))
        filer.close()
    else:
        ppid, lastFile, dnaFile = getLastFile()
        dnaModule = dnaFile[:-3]
    
    print("dnaFile: ", dnaFile)
    print("dnaModule: ", dnaModule)
    print("Parent pid: ", ppid)

    dna = importlib.import_module(dnaModule)
    
    # cellFunction.py modified time
    mTimeStart = os.path.getmtime(dnaFile)
    print("{} modified time: {}".format(dnaFile, mTimeStart))
    print("----------")
    
    # Starting point
    givenInput = dna.startNum
    currentNum = givenInput
          
    while time.time() < end_time:
    
        # Trying self-replication (typical max loop count is 120)
        random_int = random.randint(1, 120)
        if (random_int == loopCnt) or (loopCnt == 100): # One free pass at 100
            if (loopCnt == 100): # Reduce odds with "coin flip"
                random_coin = random.randint(0, 1)
                if random_coin == 1:
                    print("Won 100 50/50 coin toss, replicate. ", random_coin)
                    replicate(whoami, dnaFile, loopCnt)
                else:
                    print("Lost 100 50/50 coin toss, no replication. ", random_coin)
            else:
                print("Replicating randomly at: ", random_int)
                replicate(whoami, dnaFile, loopCnt)
        else:
            print("Random int: ", random_int)
        
        # Has the timestamp changed?
        mTimeNow = os.path.getmtime(dnaFile)

        if mTimeStart < mTimeNow:
            print("Mutate: Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason throws an error
            # Hack
            del sys.modules[dna]
            dna = importlib.import_module(dnaModule)
            #from cellFunction import cellFunction
            print("!Re-imported cellFunction")
            mTimeStart = mTimeNow
            
        print('Running: pid: {}; ppid: {}; DNA: {}; loopCnt: {}; givenInput: {}; currentNum: {}'.format(pid, ppid, dnaFile, loopCnt, givenInput, currentNum))

        # Principal cell function
        currentNum = dna.cellFunction(currentNum)

        # Write to log
        writeLog('DNA: ' + str(dnaFile) + 'loopCnt: ' + str(loopCnt) + ' givenInput: ' + str(givenInput) + ' currentNum: ' + str(currentNum) + "\n")
        
        time.sleep(1) # Small delay to reduce excessive CPU usage

        loopCnt += 1

        # Over population?
        #directory = "/home/gary/src/petri_dish/replicants"
        population = len([f for f in os.listdir(basePath) if os.path.isfile(os.path.join(basePath, f))])
        if population > MAXPOP:
            sys.exit("Max Population Exceeded: " + str(population))
