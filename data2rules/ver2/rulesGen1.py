#
# rulesGen1.py
#
#

import pickle
import pymongo


# Get data
def getPickles():

    with open('pData/starterKB.p', 'rb') as fp: # No entry for "cartoon"
        starterKB = pickle.load(fp)
        print('Aunt Bee loaded starterKB.p')
    fp.close()

    with open('pData/taggedCorpora.p', 'rb') as fp:
        taggedCorpora = pickle.load(fp)
        print('Aunt Bee loaded taggedCorpora.p')
    fp.close()
    
    return starterKB, taggedCorpora



if __name__ == "__main__":

    # Get semi-structured data
    starterKB, taggedCorpora = getPickles()

    # Get dictionary (unstructured data)
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    simpDB = myclient["simp"]
    simpDictionary = simpDB["simpDictionary"]

    #myquery = {"word": "Airplane"}
    myquery = {"word": "Aeroplane"}

    mydoc = simpDictionary.find(myquery)

    mydoccount = 0
    
    for x in mydoc:
        mydoccount += 1
        print(mydoccount, x)

    # Can we find any conclusions from the limited structured data?
    # Can we generate rules from the conclusions?
    
    # Get keys of the structured data to see what we can tally
    starterKB_Keys = starterKB[0].keys()

    print(starterKB_Keys)

    # classify?
    # We know that the KBs only have NN and NNP for tags
    nnpCount = 0
    nnCount = 0;
    errCount = 0;

    for i in starterKB:
        #print(i)
        if i["tag"] == "NNP":
            nnpCount += 1
        elif i["tag"] == "NN":
            nnCount += 1
        else:
            errCopunt += 1

    print("NNP NN Total error")
    print(nnpCount, nnCount, nnpCount + nnCount, errCount)

    # Can we do something with superclass?
    print('----- superclassGroups')

    superclassGroups = []
    
    for i in starterKB:
#        print(i)
 #       print(i["superclass"])
        if i["superclass"] not in superclassGroups:
            superclassGroups.append(i["superclass"])
    
    count = 0
    for i in superclassGroups:
        count += 1
        print(i)

    print(count)

    # Can we do something with canDo?
    print('----- canDoGroups')

    canDoGroups = []

    for i in starterKB:
#        print(i)
#        print(i["superclass"])
        if i["canDo"] not in canDoGroups:
            canDoGroups.append(i["canDo"])

    print(len(canDoGroups))
    count = 0
    for i in canDoGroups:
        count += 1
        print(i)
    print(count)

    print('- - - -')
    twoDimArr = []
    rows = len(starterKB)
    cols = len(canDoGroups)
   
    for row in range(rows):
        column = []
        for col in range(cols):
            """
            print("-", starterKB[row]["canDo"])
            if starterKB[row]["canDo"] == "compute":
                if col == 2:
                    column.append(starterKB[row])
                else:
                    column.append(0)
            else:
                column.append(0)




            TBD
            see,eat,walk,run
            compute
            see,eat,walk,run,fly
            recreation
            play
            transport
            magnify
            """
            if starterKB[row]["canDo"] == "TBD":
                if col == 0:
                    column.append(starterKB[row])
                else:
                    column.append(0)
            
            elif starterKB[row]["canDo"] == "see,eat,walk,run":
                if col == 1:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "compute":
                if col == 2:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "see,eat,walk,run,fly":
                if col == 3:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "recreation":
                if col == 4:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "play":
                if col == 4:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "transport":
                if col == 6:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            elif starterKB[row]["canDo"] == "magnify":
                if col == 7:
                    column.append(starterKB[row])
                else:
                    column.append(0)

            else:
                column.append(0)
            
            

            
        twoDimArr.append(column)

        # insert header
        if row == 0:
            twoDimArr.insert(0, canDoGroups)

    print("==========")
    for r in twoDimArr:
        print(r)
        
    print(":::::::::::")
    tbdList = []
    nonFlyList = []
    for r in twoDimArr:
        if r[0] != 0:
            tbdList.append(r[0])
        elif r[1] != 0:
            nonFlyList.append(r[1])

    print('TBD count: ', len(tbdList) - 1) # Subtract the header
    cnt = 0
    for x in tbdList:
        if cnt > 0:
            print(x)
        cnt += 1
          
    print('"see,eat,walk,run" count: ', len(nonFlyList))
    for x in nonFlyList:
        print(x)
