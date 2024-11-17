# mutator.py
#

import sys

def readFile():

    inFile = open("myInputFile.txt", "r")
    inNum = int(inFile.read())
    inFile.close()

    return inNum

def writeFile(outNum):

    outFile = open("myInputFile.txt", "w")
    outFile.writelines(str(outNum))
    outFile.close()

    return

if __name__ == "__main__":

    myInput = readFile()

    print("Current input file value: ", myInput)

    ans = input("Enter new value or CR to exit: ")

    if ans == "":
        sys.exit("Exiting without change.")
    elif ans.isnumeric():
        writeFile(ans)
        print("Input file value changed to: ", ans)
    else:
        print("Unknown input value, input file not changed.")

    print("End.")
        
