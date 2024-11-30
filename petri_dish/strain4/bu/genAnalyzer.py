# genAnalyzer.py
#
# Analyze results from generation runs.
#

import os
import pickle

from genMutator import mutate

def getFile(f):
    fileLines = []

    with open(f, 'r') as inFile:
        for line in inFile:
            fileLines.append(line.strip("\n"))
    inFile.close()
    return fileLines


if __name__ == "__main__":

    whoami = __file__

    files = []
    filesBrief = []
    keepers = []

    testChar = "/"
    res = [i for i in range(len(whoami)) if whoami.startswith(testChar, i)]
    basePath = whoami[:res[-1]]

    #path = '/path/to/directory'  # Replace with the actual path to your directory
    fileList = os.listdir(basePath)

    for f in fileList:
        if f[-3:] == "log":
            print('-----')
            print(f)

            contents = getFile(f)

            isTrue = 0
            isFalse = 0
            cnt = 1
            listOfLines = []
            reducedLines = []
            for l in contents:
                #print(l)

                lineList = l.split(',')
                #print(lineList)

                pidtmp = lineList[0].split(':')
                pid = pidtmp[1]

                ppidtmp = lineList[1].split(':')
                ppid = ppidtmp[1]

                #print(pid, ppid)

                tmpDNAFile = lineList[2].split(':')
                dnaFile = tmpDNAFile[1]

                #print(pid, ppid, dnaFile)
                
                
                if l[-4:] == "True":
                    #print("TRUE")
                    isTrue += 1
                else:
                    #print("FALSE")
                    isFalse += 1
                cnt += 1

                listOfLines.append(lineList)



            totalCnt = cnt - 1
            
            print("cnt: {}; True: {}; False: {}".format(totalCnt, isTrue, isFalse))
            X = cnt - 1
            Y = isTrue
            P = Y / X
            print("What % of {} is {}? {} or {}".format(X, Y, round(P, 2), round(P*100)))
                

            files.append((f, listOfLines))
            filesBrief.append((f, [pid, ppid, dnaFile, totalCnt, isTrue, isFalse, round(P*100)]))


    print('---------')
    print(len(files))

    #print(files[0])
    #print(files[5])

    # Save this gen's log files
    print('Saving this generation\'s logs to pickle...')
    with open("logs.p", "wb") as f:
        pickle.dump(files, f)
    f.close()
        
    print('Pickle saved.')

    print('---------')
    print(len(filesBrief))

    #print(filesBrief[0])
    highestP = 0
    for f in filesBrief:
        print('---')
        print(f)
        print(f[0])
        print(f[1])
        print('---')

        # Keep if over 40%
        #if f[1][-1] > 40:
        #    print("KEEP: ", f[1][2], f[1][-1])
        #    keepers.append((f[1][2], f[1][-1]))
        #    print(keepers)
        #else:
        #    print("DROP")

        # Keep the highest %
        if f[1][-1] > highestP:
            highestP = f[1][-1]
            keepers = [(f[1][2], f[1][-1])]

    print("K: ", keepers)
    print(keepers[0][0])

    ans = input("Mutate <Y/n>? ")
    if ans in ['Y', 'y']:
        mutate(keepers[0][0]) # Send the highestP for enhancement
    
    #print("last keeper: ", keepers[-1])
    #        
    #mutate(keepers[-1][0])

    #for k in keepers:
    #    tmp = k
    
