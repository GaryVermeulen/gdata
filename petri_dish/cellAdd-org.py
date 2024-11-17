# cellAdd.py
#
# New: Cell program test, just add by 2 for 2 minutes
# Ver2: Isolate add into a function
#

import time
import shutil


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

    shutil.copyfile(whoami, newStr)
    return

def myFunction(newNum):
    # Principal cell function
    #P!
    return newNum + 2

if __name__ == "__main__":

    newNum = 0
    myInput = 0
    newInput = 0
    
    start_time = time.time()
    end_time = start_time + 120  # 2 minutes in seconds
    
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
            
        print('Running: myInput: {}  newInput: {}  newNum: {}'.format(myInput, newInput, newNum))

        # Principal cell function
        newNum = myFunction(newNum)
        #newNum = newNum + 2
        
        writeFile(newNum)
        time.sleep(1) # Small delay to reduce excessive CPU usage
