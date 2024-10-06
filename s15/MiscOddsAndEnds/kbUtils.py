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

# Make a sudo-dataFrame--sudo since the data is not numeric
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


def canCanDo(myDataFrame, word, what):

    for d in myDataFrame:
        if d[0] == word:
            print('d: ', d)
            canDoLst = d[4].split(',')
            if what in canDoLst:
                return True

    return False


def whoCanDo(myDataFrame, what):

    aLst = []

    for d in myDataFrame:
        canDoLst = d[4].split(',')
        if what in canDoLst:
            aLst.append(d)

    return aLst


def findAncestors(myDataFrame, word):

    global tree

    print('word: ', word)

    for d in myDataFrame:
        if word == 'kbroot':
            return 
        if d[0] == word:
            tree.append(d)
            findAncestors(myDataFrame, d[5])
    return


def findChildren(myDataFrame, superclass):

    global branch

    print('superclass: ', superclass)

    for d in myDataFrame:
        if d[5] == superclass:
            branch.append(d)
            findChildren(myDataFrame, d[0])

    return
    


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

    print('-------- myDataFrame')
    print(len(myDataFrame))
    for i in myDataFrame:
        print(i)

    lst = list_isAlive(myDataFrame)

    print('-------- isAlive')
    print(len(lst))
    for i in lst:
        print(i)

    lst = list_isNonfiction(myDataFrame)

    print('-------- inNonfiction')
    print(len(lst))
    for i in lst:
        print(i)

    lst = getWord(myDataFrame, "Pookie")

    print('-------- Pookie')
    print(len(lst))
    for i in lst:
        print(i)

    lst = getSuperclass(myDataFrame, "woman")

    print('-------- superclass')
    print(len(lst))
    for i in lst:
        print(i)

    print('--------')
    print("x=y: ", isXandYsame(myDataFrame, "Mary", "Pookie"))

    print('--------')
    word = "hat"
    what = "fly"
    print("word {} can what {}: {}".format(word, what, canCanDo(myDataFrame, word, what)))

    print('-------- whoCanDo what: ', what)
    lst = whoCanDo(myDataFrame, what)

    print(len(lst))
    for i in lst:
        print(i)

    word = "Daffy"
    print('-------- findAncestors word: ', word)
    tree = []
    findAncestors(myDataFrame, word)

    print(len(tree))
    for i in tree:
        print(i)

    superclass = "animal"
    print('-------- findChildren superclass: ', superclass)
    branch = []
    findChildren(myDataFrame, superclass)

    print(len(branch))
    for i in branch:
        print(i)
