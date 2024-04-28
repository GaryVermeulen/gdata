#
# buildKB.py (Comprehension engine)
#

from commonUtils import connectMongo
from commonConfig import nnx


def connect():

    mdb = connectMongo()
    simpDB = mdb["simp"]

    return simpDB


def readStarterKB(simpDB):
    
    starterKB = simpDB["starterKB"]
    
    return list(starterKB.find({}))


def getCorpusNouns(simpDB):

    nnxLst = []

    taggedBoW = simpDB["taggedBoW"]

    bowLst = list(taggedBoW.find({}))

    for item in bowLst:
        if item["tag"] in nnx:
            nnxLst.append((item["word"], item["tag"]))
        
    return nnxLst


def findUnknownNNX(kb, nnxLst):

    kbWordLst = []
    nnxWordLst = []

    # Distill input down to word lists
    for x in kb:
        kbWordLst.append(x["_id"])

    for x in nnxLst:
        nnxWordLst.append(x[0])
        
    s = set(kbWordLst)

    unknownNNX = [x for x in nnxWordLst if x not in s]

    return unknownNNX


def findUnknownWordSents(simpDB, unknownNNX):

    allSentences = []

    taggedCorpus = simpDB["taggedCorpus"]
    taggedCorpusLst = list(taggedCorpus.find({}))

    # Convert to a list of word/tag tuples
    for s in taggedCorpusLst:
        s2 = s["taggedSentence"]
        newSent = []
        for w in s2:
            word = w["word"]
            tag  = w["tag"]
            newSent.append((word, tag))

        allSentences.append(newSent)

    # Read the tagged corpus and look for unknown nouns
    sentCnt = 0
    for s in allSentences:
        sentCnt += 1;
        print(sentCnt)
        print(s)
        for w in s:
            if w[1] in nnx:
                if w[1] != 'NNP':
                    if w[0].lower() in unknownNNX:
                        print('Unknown: ', w)
                
                        # Is it in simpDict?
                        uc = w[0].capitalize()
                        w2 = (uc, w[1])
                        dictEntry = getDictWord(simpDB, w2)
                        if len(dictEntry) > 0:
                            print('*** dictEntry: ', dictEntry)
                        else:
                            print('not found')
                else:
                    if w[0] in unknownNNX:
                        print('Unknown: ', w)
                
                        # Is it in simpDict?
                        uc = w[0].capitalize()
                        w2 = (uc, w[1])
                        dictEntry = getDictWord(simpDB, w2)
                        if len(dictEntry) > 0:
                            print('*** dictEntry: ', dictEntry)
                        else:
                            print('not found')
    return [] # allSentences


def getDictWord(simpDB, w):

    simpDict = simpDB["simpDict"]
    myQuery = {"word": w[0]}
    entry = list(simpDict.find(myQuery))

    
    #simpDictLst = list(simpDict.find({}))

    return entry
    





if __name__ == "__main__":

    print('Start buildKB...')

    simpDB = connect()
    
    kb = readStarterKB(simpDB) 
    print('kb:')
    print(len(kb))
    print(type(kb))
    for k in kb:
        print(k)    
        
    print('-' * 5)

    nnxLst = getCorpusNouns(simpDB)

    print('nnxLst:')
    print(len(nnxLst))
    print(type(nnxLst))
    for w in nnxLst:
        print(w)

    print('-' * 5)
    
    # Are these nouns in the starterKB?
    unknownNNX = findUnknownNNX(kb, nnxLst)

    print('unknownNNX:')
    print(len(unknownNNX))
    print(type(unknownNNX))
    for w in unknownNNX:
        print(w)

    print('-' * 5)
    
    # Get the tagged sentences of the unkwown words
    unknownWordSentences = findUnknownWordSents(simpDB, unknownNNX)

    print('unknownWordSentences:')
    print(len(unknownWordSentences))
    print(type(unknownWordSentences))
    for s in unknownWordSentences:
        print(s)



    print('buildKB Completed.')
