#
# rulesGen1.py
#
#

import pickle
import pymongo

import pandas as pd



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


def makeDataFrame(starterKB):

    myDataFrame = []
    index = 0
    
    for i in starterKB:
        row = []

        if index == 0:
            keys = i.keys()
            for k in keys:
                row.append(k)
        else:
            vals = i.values()            
            for v in vals:
                row.append(v)
                    
        myDataFrame.append(row)
        index += 1

    return myDataFrame

    
def list_isAlive(myDataFrame):

    aLst = []
    index = 0

    for i in myDataFrame:
        if index == 0:
            index += 1
            continue # skip header
        else:
            if i[3] == True:
                aLst.append(i)
        index += 1
        
    return aLst


def list_isNonfiction(myDataFrame):

    aLst = []
    cnt = 0

    for i in myDataFrame:
        if cnt == 0:
            cnt += 1
            continue # skip header
        else:
            if i[2] == True:
                aLst.append(i)
        cnt += 1
        
    return aLst


def getWord(myDataFrame, word):

    aLst = []

    for i in myDataFrame:
        if word == i[0]:
            aLst.append(i)

    return aLst



def getSuperclass(myDataFrame, superclass):

    aLst = []

    for i in myDataFrame:
        if superclass == i[5]:
            aLst.append(i)

    return aLst


def isXandYsame(myDataFrame, x, y):

    xLst = getWord(myDataFrame, x)
    yLst = getWord(myDataFrame, y)

    print('x: ', xLst)
    print('y: ', yLst)

    if len(xLst) != 1 or len(yLst) != 1:
        print("X or Y != 1")
        return False

    if xLst[0][5] == yLst[0][5]:
        return True

    return False
    


if __name__ == "__main__":

    # Get semi-structured data
    starterKB, taggedCorpora = getPickles()

    # Get dictionary (unstructured data)
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017")
    simpDB = myclient["simp"]
    simpDictionary = simpDB["simpDictionary"]

    #myquery = {"word": "Airplane"}
    #myquery = {"word": "Aeroplane"}
    #
    #mydoc = simpDictionary.find(myquery)
    #
    #mydoccount = 0
    #
    #for x in mydoc:
    #    mydoccount += 1
    #    print(mydoccount, x)

    # Can we find any conclusions from the limited structured data?
    # Can we generate rules from the conclusions?

    # Make our own DataFrame

    myDataFrame = makeDataFrame(starterKB)


    print(len(myDataFrame))
    for i in myDataFrame:
        print(i)

    lst = list_isAlive(myDataFrame)

    print('--------')

    print(len(lst))
    for i in lst:
        print(i)

    lst = list_isNonfiction(myDataFrame)

    print('--------')

    print(len(lst))
    for i in lst:
        print(i)



    lst = getWord(myDataFrame, "Pookie")

    print('-------- Pookie')

    print(len(lst))
    for i in lst:
        print(i)



    lst = getSuperclass(myDataFrame, "woman")

    print('--------')

    print(len(lst))
    for i in lst:
        print(i)


    print('--------')
    print("x=y: ", isXandYsame(myDataFrame, "Mary", "Pookie"))

    
    # Pandas doesn't buy us anything unles
    # we conver the strings into numbers...
    #df = pd.DataFrame(starterKB)
    #
    #print(df)
    #
    # df.corr() # Can't do this because the data is string (not numeric)
    
    """
    # My playing around...
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
                if col == 5:
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

    # Going around in circles?
    print(":::::::::::")
    tbdList = []
    nonFlyList = []
    computeList = []
    flyList = []
    recreationList = []
    playList = []
    transportList = []
    magnifyList = []
    
    for r in twoDimArr:
        if r[0] != 0:
            tbdList.append(r[0])
        elif r[1] != 0:
            nonFlyList.append(r[1])
        elif r[2] != 0:
            computeList.append(r[2])
        elif r[3] != 0:
            flyList.append(r[3])
        elif r[4] != 0:
            recreationList.append(r[4])
        elif r[5] != 0:
            playList.append(r[5])
        elif r[6] != 0:
            transportList.append(r[6])
        elif r[7] != 0:
            magnifyList.append(r[7])
        

    print('TBD count: ', len(tbdList) - 1) # Subtract the header
    cnt = 0
    for x in tbdList:
        if cnt > 0:
            print(x)
        cnt += 1
          
    print('"see,eat,walk,run" count: ', len(nonFlyList))
    for x in nonFlyList:
        print(x)

    print('compute count: ', len(computeList))
    for x in computeList:
        print(x)

    print('"see,eat,walk,run,fly" count: ', len(flyList))
    for x in flyList:
        print(x)

    print('recreation count: ', len(recreationList))
    for x in recreationList:
        print(x)

    print('play count: ', len(playList))
    for x in playList:
        print(x)

    print('transport count: ', len(transportList))
    for x in transportList:
        print(x)

    print('magnify count: ', len(magnifyList))
    for x in magnifyList:
        print(x)

    print("Total: ", len(tbdList) - 1 + len(nonFlyList) + len(computeList) + len(flyList) +
          len(recreationList) + len(playList) + len(transportList) + len(magnifyList))


    print(" Now for something different--kind of...")

    aliveList = []
    notAliveList = []
    
    for i in starterKB:
        if i["isAlive"]:
            aliveList.append(i)
        else:
            notAliveList.append(i)

    print("alive count: ", len(aliveList))
    for x in aliveList:
        print(x)
            
    print("not alive count: ", len(notAliveList))
    for x in notAliveList:
        print(x)
    """
