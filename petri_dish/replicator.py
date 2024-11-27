# replicator.py
#

import sys

def readFile():

    inFile = open("repFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum

def writeFile(outNum):

    outFile = open("repFile.txt", "w")
    outFile.writelines(str(outNum))
    outFile.close()

    return

if __name__ == "__main__":

    myInput = readFile()

    print("Current replicate file value: ", myInput)

    ans = input("Enter new value or CR to exi3t: ")

    if ans == "":
        sys.exit("Exiting without change.")
    elif ans.isnumeric():
        writeFile(ans)
        print("Replicate file value changed to: ", ans)
    else:
        print("Unknown input value, replicate file not changed.")

    print("End.")
        
