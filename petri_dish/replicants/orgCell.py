# orgCell.py
#
# Modified cellAdd.py
#

import os
import sys
import time
import shutil
import random
import importlib
from subprocess import call
from cellFunction import cellFunction

pid = os.getpid()

def readFile():

    inFile = open("../myInputFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum


def writeLog(outNum):

    whoami = __file__
    baseStr = whoami[:-3] # remove the .py
    newStr = baseStr + ".log"
    outFile = open(newStr, "a")
    outFile.writelines(str(outNum))
    outFile.close()

    return


def replicate(num):

    whoami = __file__
    testChar = "/"

    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    newStr = whoami[:res[-1]]
    newFile = newStr + "/rep" + str(pid) + "-" + str(num) + ".py"
    print("newFile (is replicant): ", newFile)

    # Create file and place in replicants folder
    shutil.copyfile(whoami, newFile)

    print("Starting replicated file: ", newFile)

    callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + newFile + "; bash"
    call(callStr)
    
    return


if __name__ == "__main__":

    MAXPOP = 50

    newNum = 0
    myInput = 0
    
    loopCnt = 1
    
    start_time = time.time()
    end_time = start_time + 120  # 2 minutes

    # cellFunction.py modified time
    mTimeStart = os.path.getmtime("cellFunction.py")
    print("cellFunction.py modified time: ", mTimeStart)
    
    # Starting point
    myInput = readFile()
    #newNum = myInput

    while time.time() < end_time:
    
        # Trying self-replication (typical max loop count is 120)
        random_int = random.randint(1, 120)
        if (random_int == loopCnt) or (loopCnt == 100): # One free pass at 100
            if (loopCnt == 200): # Reduce odds with "coin flip"
                random_coin = random.randint(0, 1)
                if random_coin == 1:
                    print("Won 200 coin toss, replicate. ", random_coin)
                    replicate(loopCnt)
                else:
                    print("Lost 200 coin toss, no replication. ", random_coin)
            else:
                print("Replicating randomly at: ", random_int)
                replicate(loopCnt)
        else:
            print("Random int: ", random_int)
        
        # Has the timestamp changed?
        mTimeNow = os.path.getmtime("cellFunction.py")

        if mTimeStart < mTimeNow:
            print("Start time < time now")
            #importlib.reload(cellFunction) # For some unkonwn reason throws an error
            # Hack
            del sys.modules['cellFunction']
            from cellFunction import cellFunction
            print("!Re-imported cellFunction")
            mTimeStart = mTimeNow
            
        print('Running: pid: {}; loopCnt: {}; myInput: {}; newNum: {}'.format(pid, loopCnt, myInput, newNum))

        # Principal cell function
        newNum = cellFunction(newNum)

        # Write to log
        writeLog('pid: ' + str(pid) + 'loopCnt: ' + str(loopCnt) + ' myInput: ' + str(myInput) + ' newNum: ' + str(newNum) + "\n")
        
        time.sleep(1) # Small delay to reduce excessive CPU usage

        loopCnt += 1

        # Over population?
        directory = "/home/gary/src/petri_dish/replicants"
        population = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
        if population > MAXPOP:
            sys.exit("Max Population Exceeded: " + str(population))
