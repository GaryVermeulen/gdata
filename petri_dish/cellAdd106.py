# cellAdd.py
#
# New: Cell program test, just add by 2 for 2 minutes
# Ver2: Isolate add into a function module that can be modified while running
#

import os
import sys
import time
import shutil
import importlib
from cellFunction import cellFunction


def readFile():

    inFile = open("myInputFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum

def writeFile(outNum):

#    outFile = open("myOutputFileAdd.txt", "w")

    whoami = __file__
    baseStr = whoami[:-3] # remove the .py
    newStr = baseStr + ".log"
    outFile = open(newStr, "w")
    outFile.writelines(str(outNum))
    outFile.close()

    return

def readRepFile():
    # Read current value
    repFile = open("repFile.txt", "r")
    repValue = int(repFile.read())
    repFile.close()

    if repValue != 0:
        # Reset to non-zero, so as not to replicate forever
        repFile = open("repFile.txt", "w")
        repFile.writelines(str(0))
        repFile.close()
    
    return repValue

def replicate(num):

    whoami = __file__
    baseStr = whoami[:-3] # remove the .py
    newStr = baseStr + str(num) + ".py"
    print("newStr: ", newStr)

    # Save replicated filename to file for Inanna
    outFile = open("repFilename.txt", "w")
    outFile.write(newStr)
    outFile.close()

    # Create file
    shutil.copyfile(whoami, newStr)
    return

#def myFunction(newNum):
#    # Principal cell function
#    #P!
#    return newNum + 2

if __name__ == "__main__":

    newNum = 0
    myInput = 0
    newInput = 0
    
    start_time = time.time()
    end_time = start_time + 120  # 2 minutes in seconds

    # cellFunction.py modified time
    mTimeStart = os.path.getmtime("cellFunction.py")
    print("cellFunction.py modified time: ", mTimeStart)
    
    # Starting point
    myInput = readFile()
    newNum = myInput

    while time.time() < end_time:
        # Has inputFile been mutated?
        newInput = readFile()
        if newInput != myInput:
            myInput = newInput
            newNum = newInput

        if readRepFile() != 0:
            print("Replicate")
            replicate(newNum)

        mTimeNow = os.path.getmtime("cellFunction.py")

        if mTimeStart < mTimeNow:
            print("Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason throws an error
            # Hack
            del sys.modules['cellFunction']
            from cellFunction import cellFunction
            print("!Re-imported cellFunction")
            mTimeStart = mTimeNow
            
        print('Running: myInput: {}  newInput: {}  newNum: {}'.format(myInput, newInput, newNum))

        # Principal cell function
        newNum = cellFunction(newNum)
        #newNum = myFunction(newNum)
        #newNum = newNum + 2
        
        writeFile(newNum)
        time.sleep(1) # Small delay to reduce excessive CPU usage
