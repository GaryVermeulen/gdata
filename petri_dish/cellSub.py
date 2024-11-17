# cellSub.py
#
# Cell program test, just subtract by 2 for 2 minutes
#

import time


def readFile():

    inFile = open("myInputFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum

def writeFile(outNum):

    outFile = open("myOutputFileSub.txt", "w")
    outFile.writelines(str(outNum))
    outFile.close()

    return



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
            
        print('Running: myInput: {}  newInput: {}  newNum: {}'.format(myInput, newInput, newNum))
        newNum = newNum - 2
        writeFile(newNum)
        time.sleep(1) # Small delay to reduce excessive CPU usage
