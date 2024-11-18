# inanna.py
# V1:
# Consolidate cell mutator and replicator functionality
#

import os
import sys
import time
from subprocess import call


def start():

    print("Start (cellAdd.py).")

    #os.system("x-terminal-emulator -e 'bash -c \"echo Opening a new terminal; exec bash\"'")

    call(["gnome-terminal", "-x", "sh", "-c", "python3 cellAdd.py; bash"])

    return

def mutate():

    print("Mutate.")

    return

def replicate():

    print("Replaicate.")

    myInput = readRepFile()

    print("Current replicate file value: ", myInput)
    ans = input("Enter new value or CR to exit: ")

    if ans == "":
        #sys.exit("Exiting without change.")
        print("Exiting without change.")
    elif ans.isnumeric():
        writeRepFile(ans)
        print("Replicate file value changed to: ", ans)

        # Wait for replicated filename to be written to file
        time.sleep(1)
        # WHat is the name of the replicated file?
        repFile = open("repFilename.txt", "r")
        repName = repFile.read()
        repFile.close()

        print("Starting replicated file: ", repName)

        callStr = "gnome-terminal", "-x", "sh", "-c", "python3 " + repName + "; bash"
        
        #call(["gnome-terminal", "-x", "sh", "-c", "python3 ", repName, "; bash"])

        call(callStr)
        
    else:
        print("Unknown input value, replicate file not changed.")

    return

def readRepFile():

    inFile = open("repFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum

def writeRepFile(outNum):

    outFile = open("repFile.txt", "w")
    outFile.write(str(outNum))
    outFile.close()

    return

if __name__ == "__main__":
    
    cont = True

    print("I am Inanna, and I can grant you three wishes. Choose wisely... ")

    while cont:
        choice = input("Mutate, Replicate, Start (addCell.py), or leave in peace <M/R/S/x>: ")

        if choice not in ['r', 'R', 'm', 'M', 's', 'S']:
            sys.exit("Exiting, leave in peace.")
        elif choice in ['r', 'R']:
            replicate()
        elif choice in ['m', 'M']:
            mutate()
        elif choice in ['s', 'S']:
            start()
        else:
            sys.exit("Exiting, shoud not really get here?!?! ", choice)
        
