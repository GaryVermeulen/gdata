# filer.py
#




if __name__ == "__main__":

    fileName = "cell1Body.py"
    dnaFile = "cell1DNA.py"

    fileEntry = fileName + "," + dnaFile + "\n"

    filer = open("fileList.txt", "w")
    filer.writelines(fileEntry)
    filer.close()


    inF = open("fileList.txt", "r")
    inFile = inF.read()
    inF.close()

    print(inFile)

    print('------')

    fileName = "cell23180Body.py"
    dnaFile = "cell23180DNA.py"

    fileEntry = fileName + "," + dnaFile + "\n"

    filer = open("fileList.txt", "a")
    filer.writelines(fileEntry)
    filer.close()

    fLst = []
    with open("fileList.txt", "r") as f:
        for line in f:
            print('line: ', line.strip())
            line = line.replace("\n", "")
            lineLst = line.split(',')
            print('lineLst: ', lineLst)
            fLst.append(lineLst)
    f.close()

    for l in fLst:
        print(l)


    print("last: ", fLst[-1])
    lastFile = fLst[-1][0]
    lastDNA = fLst[-1][1]

    print("lastFile: " , lastFile)
    print("lastDNA: " , lastDNA)

    bx = [i for i in range(len(lastFile)) if lastFile.startswith("B", i)]
    print(bx)
    bIdx = bx[0]
    cIdx = 0

    head = lastFile[:4] # pick off cell
    tail = lastFile[-7:] # pick off Body.py
    
    print(head)
    print(tail)
    
    num = lastFile[cIdx + 4:bIdx]

    print(num)

    nextNum = int(num) + 1

    print(nextNum)

    
    

    
