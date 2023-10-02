#
# rectifyKB.py
#
# 1) Check for tagging errors in BoW and tagged senetences
#       Currently only checking on lower case NNPs
# 2) Verify and add NN and NNPs in BoW but not in KB
#       This could be can of worms--cannot do this without knowing
#       canDo, isAlive, and superclass
#
# Yet again this has morphed so now wondering if it would make more sense
# to recify during the initial reading and processing of the raw corpus...~?
#
# This is really ugly, but in a sick way: fun.
#

import pickle

from commonUtils import connectMongo, listSuperclasses, listKB_Entries, isEntry, getEntryAll, isEntryBoW, getEntryAllBoW 
                        
from commonConfig import validTags, nnx

from scrapeWord import scrapeWord
from addWebWords import addWebWord
from simpSA import sentAnalysis



def lowerCase_NNP_Check(tagged_BoW):
    # Simplw check of NNPs in BoW--Are there any uncapitalized NNPs?

    print('- lowerCase_NNP_Check - Start -')
    
    result = ''
    chkList = []
    validInput = validTags.copy()
    validInput.append('C') # Capitalize
    validInput.append('c')
    validInput.append('K') # Keep as is
    validInput.append('k')
        
    cursor = tagged_BoW.find({"tag": "NNP"})

    # Simple check: Is the first char capitalized?
    for doc in cursor:
        if doc["word"][0].islower():
            print('-' * 10)
            print('Found uncapitalized NNP:', doc["word"])

            while result not in validInput:
                result = input('Enter correct POS tag, C/c to capitalize, or K/k to keep as is: ')
                
            if result in validTags:
                doc["tag"] = result
                print('Re-tagged: {} as: {} '.format(doc["word"], doc["tag"]))

            if result in ['C', 'c']:
                doc["word"] = doc["word"].capitalize()
                print('New case (upCase):')
                print('Re-cased word: {}  Tag: {} '.format(doc["word"], doc["tag"]))

            if result in ['K', 'k']:
                print('Keeping {} {} as is.'.format(doc["word"], doc["tag"]))

            chkList.append(doc)
            result = ''

    # Update MongoDB
    for w in chkList:
        print('Replacing:')
        print(w)
        q = {"_id": w["_id"]}
        
        result = tagged_BoW.replace_one(q, {"word": w["word"], "tag": w["tag"]})

        print('Raw result: ', result.raw_result)
        print('Acknowledged: ', result.acknowledged)
        print('Macthed count: ', result.matched_count)

    print('- lowerCase_NNP_Check - End -')
    return


def makeEntry(taggedWord):

    tmpDict = {}

    if len(taggedWord) == 0:
        word = input("Enter word: ")
        if len(word) == 0:
            print('Nothing entered, existing...')
            return {}
        tag = input('Enter valid POS tag: ')
        if tag in validTags:
            print('Tagged: {} as: {} '.format(word, tag))
        else:
            tag = 'UNK'
            print('Invalid tag entered, tagging as: ', tag)
    else:
        word = taggedWord[0]
        tag = taggedWord[1]
    
    modRes = input('Modify word/tag <Y/n>?')
    if modRes in ['y', 'Y']:
        caseRes = input('Lower case {} <Y/n>?'.format(word))
        if caseRes in ['y', 'Y']:
            word = word.lower()
        tagRes = input('Change the POS tag for {} <Y/n> WARNING KB only handles NN and NNP '.format(taggedWord))
        if tagRes in ['y', 'Y']:
            r = input('Enter valid POS tag: ')
            if r in validTags:
                tag = r
                print('Re-tagged: {} as: {} '.format(word, tag))
            else:
                print('Invalid tag entered, keeping: ', tag)
            
    sims = input('Enter similars: word1,word2,...')
    isA = input('Enter isAlive: <T/F>')
    if isA in ['t', 'T']:
        isA = True
    canD = input('Enter canDo: see,eat,run,...')

    print('Valid superclasses:')
    nodeList = listKB_Entries(nnxKB)

    superC = input('Enter superClass/parent: ')

    if superC not in nodeList:
        print('No {} found! You will need to manually add the superclass.'.format(superC))
        return {}

    tmpDict = {
        "_id":word,
        "similar":sims,
        "tag":tag,
        "isAlive": isA,
        "canDo":canD,
        "superclass":superC
    }

    return tmpDict


def nnpNotInKB(tagged_BoW, nnxKB):

    print('- nnpNotInKB Start -')
    toAdd = []
    cursor_nnp_BoW = tagged_BoW.find({"tag": "NNP"})
    cursor_nnp_KB = nnxKB.find({"tag": "NNP"})

    print(' --- Searching for NNPs in BoW that are not in KB ---')
    
    for docBoW in cursor_nnp_BoW:
#        print(docBoW)
        toAdd.append(docBoW)
        c = nnxKB.find({"_id": docBoW["word"]})
        for i in c:
#            print('match:', i)
            toAdd.pop()

    print(' --- Found these: toAdd ---')
    for i in toAdd:
        print(i)

    print('-' * 10)
    print('Found {} words that are in BoW but not in the KB'.format(len(toAdd)))
    result = input('Enter <Y/y> to add?')

    newWords = []
    if result in ['y', 'Y']:
        for entry in toAdd:
            word = entry["word"]
            tag  = entry["tag"]
            taggedWord = (word, tag)
            isA = False
                         
            print('.............................................')

            # Check if already in KB
            print('Checking taggedWord: ', taggedWord)
            
            if isEntry(taggedWord, nnxKB):
                allEntries = getEntryAll(taggedWord, nnxKB)

                if len(allEntries) > 0:
                    for e in allEntries:
                        print("Warning: {} is in the KB ".format(e))
                    continue

            contRes = input('Continue with add/modify {} <Y/n>?'.format(taggedWord))
            if contRes in ['y', 'Y']:

                tmpDict = makeEntry(taggedWord)

                if len(tmpDict) < 1:
                    print('Bad entry, skipping ', taggedWord)
                    continue
                
                print('You have entered:')
                print('word      : ', tmpDict["_id"])
                print('tag       : ', tmpDict["tag"])
                print('similars  : ', tmpDict["similar"])
                print('isAlive   : ', tmpDict["isAlive"])
                print('canDo     : ', tmpDict["canDo"])
                print('superclass: ', tmpDict["superclass"])

                inRes = input('Add this to KB <Y/n>?')

                if inRes not in ['y', 'Y']:
                    continue
                
                insertResult = nnxKB.insert_one(tmpDict)
                print('Raw insertResult acknowledged: ', insertResult.acknowledged)
                    
            else:
                print('Skipping... ',taggedWord)
    
    print('- nnxNotInKB End -')

    return


def nnNotInKB(tagged_BoW, nnxKB, webWordsCol):

    print('- nnNotInKB Start -')
    toAddRaw = []
    toAddNotInKB = []
    toAdd = []
    multipleBoW = []
    cursor_nn_BoW = tagged_BoW.find({"tag": "NN"})
    cursor_nn_KB = nnxKB.find({"tag": "NN"})

    print(' --- Searching for NNs in BoW that are not in KB ---')
    
    for docBoW in cursor_nn_BoW:
#        print(docBoW)
        toAddRaw.append(docBoW)
        c = nnxKB.find({"_id": docBoW["word"]})
        for i in c: 
#            print('match:', i)
            toAddRaw.pop()

    # Check if in KB with different case
    print('len toAddRaw: ', len(toAddRaw))
    for i in toAddRaw:
        taggedWord = (i["word"],i["tag"])
        
#        print('Checking taggedWord: ', taggedWord)
            
        if isEntry(taggedWord, nnxKB):
            allEntries = getEntryAll(taggedWord, nnxKB)

            if len(allEntries) > 0:
                for e in allEntries:
                    print("Warning: {} is in the KB skipping...".format(e))
        else:
            toAddNotInKB.append(i)

    # Check if in BoW with different case
    print('len toAddNotInKB: ', len(toAddNotInKB))
    for i in toAddNotInKB:
        taggedWord = (i["word"],i["tag"])
        
#        print('Checking taggedWord: ', taggedWord)
            
        if isEntryBoW(taggedWord, tagged_BoW):
            allEntries = getEntryAllBoW(taggedWord, tagged_BoW)

            if len(allEntries) > 1:
                for e in allEntries:
#                    print("Warning: {} is in the KB...".format(e))
                    multipleBoW.append(e)
            else:
                toAdd.append(i)
                
    print(' --- Found multiple entries in BoW ---')
    for e in multipleBoW:
        print(e)
    
    print(' --- Found these: toAdd ---')
    print('len toAdd: ', len(toAdd))
    for i in toAdd:
        print(i)

    print('-' * 10)
    print('Found {} words (NN) not in KB?'.format(len(toAdd)))

    # Are they in webWords?
    addWebWords = []
    

    for i in toAdd:
        taggedWord = (i["word"],i["tag"])

        c = list(webWordsCol.find({"word": i["word"]}))

        if len(c) == 0:
            addWebWords.append(i)
        

    print('-' * 10)
    for i in addWebWords:
        print(i)
    print('Found {} words (NN) not in webWordsCol?'.format(len(addWebWords)))
    
    result = input('Scrape web <Y/n>?')

    newWords = []
    if result in ['y', 'Y']:
        for entry in addWebWords:
            word = entry["word"]
            tag  = entry["tag"]
            taggedWord = (word, tag)
                         
            print('.............................................')
            #newWord = scrapeNNX(taggedWord)
            newWord = scrapeWord(taggedWord)
            if len(newWord) > 0:
                newWords.append(newWord)
        print('-' * 10)
        print('len newWords: ', len(newWords))
        print('newWords:')
        for w in newWords:
            print(w)

        # Save for testing and debugging
        print('-' * 10)
        print('Saving scraped words [newWords] object:')
        f = open('pickles/newWords.pkl', 'wb')
        pickle.dump(newWords, f)
        f.close()
        print('Aunt Bee saved newWords.pkl')

        print('-' * 10)
        print('Add {} words the above to the KB?'.format(len(newWords)))
        result = input('Add words <Y/n>?')
        if result in ['y', 'Y']:
            print('check/mod addNNX')
            for w in newWords:
                print('Sending w: ', w)
                addWebWord(w)
            
    else:
        print('Missing words not added to KB.')

    print('-' * 10)
    print('Added: len newWords: ', len(newWords))
    
    print('- nnNotInKB End -')

    return


def addKBNode(nnxKB):

    print('- addKBNode Start -')

    newNode = makeEntry('')

    if len(newNode) < 1:
        print('Bad entry, skipping...')
        return
                
    print('You have entered:')
    print('word      : ', newNode["_id"])
    print('tag       : ', newNode["tag"])
    print('similars  : ', newNode["similar"])
    print('isAlive   : ', newNode["isAlive"])
    print('canDo     : ', newNode["canDo"])
    print('superclass: ', newNode["superclass"])

    res = input('Add this to KB <Y/n>?')

    if res not in ['y', 'Y']:
        return
                
    insertResult = nnxKB.insert_one(newNode)
    print('Raw insertResult acknowledged: ', insertResult.acknowledged)            

    print('- addKBNode End -')

    return


def bow_dif_nnxKB(tagged_BoW, nnxKB, webWordsCol):

    toAddRaw = []
    toAddNotInKB = []
    toAdd = []
    multipleBoW = []

    cursor_nn_BoW = tagged_BoW.find({"tag": "NN"})

    for docBoW in cursor_nn_BoW:
#        print(docBoW)
        toAddRaw.append(docBoW)
        c = nnxKB.find({"_id": docBoW["word"]})
        for i in c: 
#            print('match:', i)
            toAddRaw.pop()

    # Check if in KB with different case
#    print('len toAddRaw: ', len(toAddRaw))
    for i in toAddRaw:
        taggedWord = (i["word"],i["tag"])
        
#        print('Checking taggedWord: ', taggedWord)
            
        if isEntry(taggedWord, nnxKB):
            allEntries = getEntryAll(taggedWord, nnxKB)

            if len(allEntries) > 0:
                for e in allEntries:
                    print("Warning: {} is in the KB skipping...".format(e))
        else:
            toAddNotInKB.append(i)

    # Check if in BoW with different case
#    print('len toAddNotInKB: ', len(toAddNotInKB))
    for i in toAddNotInKB:
        taggedWord = (i["word"],i["tag"])
        
#        print('Checking taggedWord: ', taggedWord)
            
        if isEntryBoW(taggedWord, tagged_BoW):
            allEntries = getEntryAllBoW(taggedWord, tagged_BoW)

            if len(allEntries) > 1:
                for e in allEntries:
#                    print("Warning: {} is in the KB...".format(e))
                    multipleBoW.append(e)
            else:
                toAdd.append(i)
                
#    print(' --- Found multiple entries in BoW ---')
#    for e in multipleBoW:
#        print(e)
    
#    print(' --- Found these: toAdd ---')
#    print('len toAdd: ', len(toAdd))
#    for i in toAdd:
#        print(i)

#    print('-' * 10)
#    print('Found {} words (NN) not in KB?'.format(len(toAdd)))



    return toAdd, multipleBoW


def prepareSentences(found):

    listOfSents = []

    for s in found:
        print('s: ', s)
        tmpSent = []
        ts = s["taggedSentence"]
        for word in ts:
            #tmpSent = []
            print('word: ', word)
            taggedWord = (word["word"], word["tag"])
            tmpSent.append(taggedWord)
            
        listOfSents.append(tmpSent)
    print('ps---')        
    for i in listOfSents:
        print(i)

    return listOfSents


def rectifyKB(tagged_BoW, tagged_Corpus, webWordsCol, nnxKB):
    # Attempt to add KB entries from the above input.
    # I'm guessing we'll need to try and glean the needed
    # missing KB info (isAlive, canDo, and superclass from
    # the webWordsCol and tagged_Corpus

    limit = 0
    found = []
    saObjLst = [] # List of saObj's

    print('--- rectifyKB Start ---')

    toAdd, multipleEntries = bow_dif_nnxKB(tagged_BoW, nnxKB, webWordsCol)

    print('len toAdd: ', len(toAdd))
    print('len multipleEntries: ', len(multipleEntries))

    # Retrieve sentences from taggedCorpus containing word to add. Then try to
    # derive context...

    for entry in toAdd:

        print(type(entry))
        print('entry: ', entry)
        word = entry["word"]
        tag = entry["tag"]

        print("word: ", word)
        print("tag: ", tag)
        print('-' * 5)

        wordCur = list(tagged_Corpus.find())

        print(type(wordCur))
        l2 = 0
        
        for c in wordCur:
#            print(type(c))
#            print("c: ", c)

            cTS = c["taggedSentence"]

#            print(type(cTS))
#            print(cTS)

            for x in cTS:
                x_entry = x["word"]
#                print(x_entry)
                if x_entry == word:
                    print('match: ')
                    print(word, x_entry)
                    found.append(c)

        listOfSentences = prepareSentences(found) # Prepare for smipSA

        for sent in listOfSentences:
            saObj, error = sentAnalysis(sent) # Just one sent at a time
            print('--')
            print('error: ', error)
            saObj.printAll()
            saObjLst.append(saObj)

        print('len saObjLst: ', len(saObjLst))
        
            
        limit += 1
        if limit > 0:
            break # Just trying to process one for now

    print('saObj lst:')
    for i in saObjLst:
        i.printAll()



    print('--- rectifyKB End ---')

    return


#
#
if __name__ == "__main__":

    print('--- Start rectifyKB.py ---')
    result = ''
    mdb = connectMongo()
    simpDB = mdb["simp"]
    nnxKB = simpDB["nnxKB"]
    tagged_BoW = simpDB["taggedBoW"]
    taggedCorpus = simpDB["taggedCorpus"]
    webWordsCol = simpDB["webWords"]

    while result not in ['1', '2', '0']:
        print('   1 -- Case check NNPs in BoW')
        print('   2 -- Check for NNPs in BoW that are not in KB')
        print('   3 -- Check for NNs in BoW that are not in KB')
        print('   4 -- Add KB object (superclass) not in corpus')
        print('   5 -- Auto-add words form corpus & webWords to KB')
        print('   0 -- Exit')
        result = input('Enter choice: ')
        if result == '1':
            lowerCase_NNP_Check(tagged_BoW)
        elif result == '2':
            nnpNotInKB(tagged_BoW, nnxKB)
        elif result == '3':
            nnNotInKB(tagged_BoW, nnxKB, webWordsCol)
        elif result == '4':
            addKBNode(nnxKB)
        elif result == '5':
            rectifyKB(tagged_BoW, taggedCorpus, webWordsCol, nnxKB)
        elif result == '0':
            print('Exiting...')
            break
        else:
            print('Something really wrong since you should not be able to get here')
        result = ''

    print('--- End   rectifyKB.py ---')
