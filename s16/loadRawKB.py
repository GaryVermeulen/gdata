#
# loadRawKB.py
#
# Loads KB text file
#
# New: 11/10/24
#

import pickle

pickleFile = 'pickleJar/starterKB.p'

def loadRawKB():
    # Read the ordered starter kb file
    # For now only handling NNPs and NNs--we'll deal with plurals later

    kbList = []
    vocabList = []
    isAlive = False
    
    with open('inputData/starterKB.txt', 'r') as f:
        while (line := f.readline().rstrip()):
            if line[0] == '#': # Skip comments
                continue
            else:
                tmp = line.split(';')
                #print('tmp: ', tmp)
                if tmp[2] == "T":
                    isNonfiction = True
                else:
                    isNonfiction = False
                    
                if tmp[3] == "T":
                    isAlive = True
                else:
                    isAlive = False
                    
                tmpDict = {
                    #"_id":tmp[0],
                    "word": tmp[0],
                    "tag": tmp[1],
                    "isNonfiction": isNonfiction,
                    "isAlive": isAlive,
                    "canDo": tmp[4],
                    "superclass": tmp[5]
                }
                kbList.append(tmpDict)
                #vocabList.append(tmp) # If a list is needed
    f.close()
                                   
    #return kbList, vocabList
    return kbList



if __name__ == "__main__":

    print('START: load')
    
    kb = loadRawKB() 
    print('kb:')
    print(len(kb))
    print(type(kb))

    print('kB ------------------------')
    for k in kb:
        print(k)

    print('dumping kb to pickle...')
    with open(pickleFile, "wb") as f:
        pickle.dump(kb, f)
    
    print('------------')

    print('loadRawKB Complete.')
