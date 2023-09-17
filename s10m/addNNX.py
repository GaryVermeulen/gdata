#
# addNNX.py
#
#   Take word from scrapeNNX and add to nnxKB.
#

import sys
import pickle

from commonUtils import connectMongo


def listSuperclasses(all_nnxKB):

    superClassList = []

    for i in all_nnxKB:
        if i["superclass"] not in superClassList:
            if i["superclass"] != None: # root does not have a superclass
                superClassList.append(i["superclass"])
                
    for i in superClassList:
        print(i)

    return superClassList


def findSimilars(similars):

    wordStack = []
    onStack = False
    threshold = 1
    freq = ''
    
    # Make a list of words and their freq
    for s in similars:
        onStack = False
        s_taggedWord = s["word"]
        s_similars = s["similars"]
        
        for word in s_similars:
            tmpWord = {"word": word, "cnt": 1}

            for w in wordStack:
                if w["word"] == tmpWord["word"]:
                    w["cnt"] = w["cnt"] + 1
                    onStack = True
                    break

            if not onStack:
                wordStack.append(tmpWord)
                
    for w in wordStack:
        print(w)
        if w["cnt"] > threshold:
            if len(freq) == 0:
                freq = w["word"]
            else:
                freq = freq + "," + w["word"]
    print('---')
    print(freq)
                
    return freq


def addNNX(newWordDef):

    result = ''
    similar = ''
    isAlive = False
    canDo = 'TBD'
    superClass = ''
    mdb    = connectMongo()
    simpDB = mdb["simp"]
    nnxKB  = simpDB["nnxKB"]

    # Get all entries for listing canDo's and superclasses
    all_nnxKB = list(nnxKB.find())
    print('nnxKB has {} entries.'.format(len(all_nnxKB)))

    # Make sure new word is not in NNXKB
    newTaggedWord = newWordDef[0]["word"]

    print("newTaggedWord: ", newTaggedWord)
    print("word: ", newTaggedWord[0])
    print("tag: ", newTaggedWord[1])

    node = list(nnxKB.find({"_id":newTaggedWord[0]}))

    if len(node) == 0:
        print('Could not find a node named: ', newTaggedWord[0])
    else:
        print('Found {} in nnxKB'.format(newTaggedWord[0]))
        for i in node:
            print(i)
        sys.exit("{} Exists in nnxKB, exiting.".format(newTaggedWord[0]))
   
    print('newWordDef:')
    for i in newWordDef:
        print(i)

    print('-' * 5)
    similar = findSimilars(newWordDef)
    print('similar:')
    print(similar)

    print('-' * 5)
    print("Input needed: isAlive? canDo? superClass?")
    result = input("Continue with add? <Y/N>")
    if result not in ['y', 'Y']:
        print('*** Add aborted.')
        return 'Add aborted.'
    
    while result not in ['t', 'T', 'f', 'F']:
        result = input("Enter T/F for isAlive? ")

    if result in ['t', 'T']:
        isAlive = True
    print('isAlive: ', isAlive)
    
    print('-' * 5)
    result = ''
    while result not in ['y', 'Y']:

        print('WARNING: This is cheesy - enter: word1,word2,word3 or TBD') 
        canDo = input("Enter canDo <see|eat|walk|run|fly|compute|recreation|play|transport|magnify|TBD> ")

        print('canDo: ', canDo)
        result = input('Is the above correct for canDo? <Y/N> ')
    print('Accepted canDo: ', canDo)

    print('-' * 5)
    print('Valid superclasses:')
    superClassList = listSuperclasses(all_nnxKB)

    while result not in superClassList:
        result = input("Enter superclass? ")

    superClass = result
    print('suppclass: ', superClass)

    tmpDict = {
                    "_id":newTaggedWord[0],
                    "similar":similar,
                    "tag":newTaggedWord[1],
                    "isAlive": isAlive,
                    "canDo":canDo,
                    "superclass":superClass
                }
    
    print('tmpDict:')
    print(tmpDict)
    result = ''
    while result not in ['y', 'Y', 'n', 'N']:
        result = input('Add to nnXKB? <Y/N> ')
        
    if result in ['y', 'Y']:
        nnxKB.insert_one(tmpDict)
        print('Inserted.')
        return 'Inserted.'
    else:
        print('Not inserted.')
        return 'Not inserted.'
    

    return "?Unknown?"



if __name__ == "__main__":

    print('-- Start: addNNX.py __main__ ')

    # Test input
    """
    newWordDef = [
        {'word': ('boy', 'NN'), 'similars': ['male', 'child', 'birth', 'adulthood']},
        {'word': ('boy', 'NN'), 'similars': ['child', 'gender', 'identity', 'male']},
        {'word': ('boy', 'NN'), 'similars': ['son']},
        {'word': ('boy', 'NN'), 'similars': ['immature', 'male']},
        {'word': ('boy', 'NN'), 'similars': ['male', 'romantic', 'partner', 'boyfriend']},
        {'word': ('boy', 'NN'), 'similars': ['man', 'boy', 'native', 'place']},
        {'word': ('boy', 'NN'), 'similars': ['man', 'person']},
        {'word': ('boy', 'NN'), 'similars': ['close', 'male', 'friend']},
        {'word': ('boy', 'NN'), 'similars': ['male', 'animal', 'pet']},
        {'word': ('boy', 'NN'), 'similars': ['male', 'servant', 'man']}
        ]
    """
    """
    newWordDef = [{'word': ('man', 'NN'), 'similars': ['male', 'gentleman', 'guy', 'fellow', 'bloke', 'lad']}]
    """

    # Load pickle saved in rectifyKB
    with open('pickles/newWords.pkl', 'rb') as fp:
        newWords = pickle.load(fp)
        print('Aunt Bee loaded newWords.pkl')
    fp.close()

    for newWordDef in newWords:
        results = addNNX(newWordDef)


    print('-- End: addNNX.py __main__ ')
