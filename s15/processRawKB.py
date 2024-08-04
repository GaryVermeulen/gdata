#
# processRawKB.py
#
# Builds starterKB and simpVocabulary Mongo collections
#

from commonUtils import connectMongo
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
                print('tmp: ', tmp)
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
                vocabList.append(tmp)
    f.close()
                                   
    return kbList, vocabList


def buildMongoKB(kb):
    
    # Save to Mongo
    mdb = connectMongo()
    simpDB = mdb["simp"]
    starterKB = simpDB["starterKB"]

    # For now start fresh every run
    starterKB.drop()

    starterKB.insert_many(kb)

    return "Added KB to simp"


def buildVocab(vocabList):

    mdb = connectMongo()
    simpDB = mdb["simp"]
    simpDictionary = simpDB["simpDictionary"]
    simpVocabulary = simpDB["simpVocabulary"]

    simpVocabulary.drop()

    for wordList in vocabList:
        #print('wordList: ', wordList)

        word = wordList[0]
        tag = wordList[1]
        capWord = word.capitalize()

        #print('word: ', word)
        #print('capWord: ', capWord)
        #print('tag: ', tag)

        query = {"word": capWord}
        doc = list(simpDictionary.find(query))
        #print('doc: ', doc)
    
        if len(doc) > 0:
            for d in doc:
                #print('d: ', d)
                #print('d["word"]: ', d["word"])
                #print('d["tag"]: ', d["tag"])
                #print('d["definition"]: ')
                #print(d["definition"])
                #print('----')

                tmpDict = {
                    "word": d["word"],
                    "tag": d["tag"],
                    "definition": d["definition"]
                    }
                x = simpVocabulary.insert_one(tmpDict)
                
        else:
            print('{} with tag {} not found in simpDictionary.'.format(word, tag))

    return "Vocab Built"

if __name__ == "__main__":

    print('Processing Starter KB...')
    
    kb, vocabList = loadRawKB() 
    print('kb:')
    print(len(kb))
    print(type(kb))
    print('vocabList:')
    print(len(vocabList))
    print(type(vocabList))

    #for x in vocabList:
    #    print(x)    
        
    print('-' * 5)

    buildVocab(vocabList)

    print('dumping kb to pickle...')
    with open(pickleFile, "wb") as f:
        pickle.dump(kb, f)
    
    print('------------')
 
    print(buildMongoKB(kb))
    

    print('processRawKB Complete.')
