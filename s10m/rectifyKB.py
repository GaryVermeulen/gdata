#
# rectifyKB.py
#
# 1) Check for tagging errors in BoW and tagged senetences
#       Currently only checking on lower case NNPs
# 2) Verify and add NN and NNPs in BoW but not in KB
#       This could be can of worms
#

import pickle

from commonUtils import connectMongo
from commonConfig import validTags, nnx
from scrapeNNX import scrapeNNX
from addNNX import addNNX


def updateTagInBoW(w, cleanTagged_BoW_List):

    print('word:', w["word"])
    print('tag: ', w["tag"])

    for i in cleanTagged_BoW_List:
        if i[0] == w["word"]:
            i[1] = w["tag"]
            print(i)
            
    return cleanTagged_BoW_List


def updateCaseInBoW(w, cleanTagged_BoW_List):

    print('word:', w["word"])
    print('tag: ', w["tag"])

    for i in cleanTagged_BoW_List:
        if i[0] == w["word"].lower():
            print('i before: ', i)
            i[0] = w["word"]
            print('i after: ', i)
    
    return cleanTagged_BoW_List


def lowerCase_NNP_Check(tagged_BoW):
    # Simplw check of NNPs in BoW--Are there any uncapitalized NNPs?

    print('- lowerCase_NNP_Check - Start -')
    
    result = ''
    validInput = validTags.copy()
    validInput.append('C') # Capitalize
    validInput.append('c')
    validInput.append('K') # Keep as is
    validInput.append('k')

    tagged_BoW_List = list(tagged_BoW.find())
        
    chkList = []
  

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


def nnpNotInKB(tagged_BoW, nnxKB):

    print('- nnxNotInKB Start -')

    totalNNX = 0
    foundNNX = 0
    notFound = 0
    noKB = [] 

    tagged_BoW_List = list(tagged_BoW.find())
    nnxKB_List = list(nnxKB.find())

    print('len BoW: ', len(tagged_BoW_List))
    print('len KB : ', len(nnxKB_List))

    bowLst = []
    for w in tagged_BoW_List:
        if w["tag"] in nnx:
            bowLst.append(w["word"])

    nnxLst = []
    for w in nnxKB_List:
        nnxLst.append(w["_id"])

    print(len(bowLst))
#    for w in bowLst:
#        print(w)

    print('---')
    print(len(nnxLst))
#    for w in nnxLst:
#        print(w)

    print('---')

    set_bow = set(bowLst)
    set_nnx = set(nnxLst)
    
    diff = set_bow.difference(set_nnx)

    print('set_bow: ', len(set_bow))
    print('set_nnx: ', len(set_nnx))    
    print('diff: ', len(diff))

    chk = len(set_bow) - len(set_nnx)
    print('chk: ', chk)

    tmpLst = []
    for b in set_bow:
        for n in set_nnx:
            #print(n)
            if b == n:
                #print('match')
                if b not in tmpLst:
                    tmpLst.append(b)

    print('tmpLst: ', len(tmpLst))
    print(tmpLst)



    print('-----')
    print(diff)

    print('-----')
    add2KBLst = []
    diffLst = list(diff)
    print(diffLst)
    
    for tWord in tagged_BoW_List:
        if tWord["word"] in list(diff):
            add2KBLst.append((tWord["word"], tWord["tag"]))

    print('-----')
    print('len add2KBLst: ', len(add2KBLst))
    print(add2KBLst)

    print('-' * 10)
    print('Scrape web for words in BoW but not in KB?')
    result = input('Scrape web <Y/n>?')

    newWords = []
    if result in ['y', 'Y']:
        for taggedWord in add2KBLst:
            if taggedWord[1] in nnx:
                print('.............................................')
                newWord = scrapeNNX(taggedWord)
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
            for w in newWords:
                addNNX(w)
            
    else:
        print('Missing words not added to KB.')

    print('-' * 10)
    
    print('Found: len add2KBLst: ', len(add2KBLst))
    print('Added: len newWords: ', len(newWords))
    
    print('- nnxNotInKB End -')

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

    while result not in ['1', '2', '0']:
        print('   1 -- Case check NNPs in BoW')
        print('   2 -- Check for NNPs in BoW that are not in KB')
        print('   3 -- Check for NNs in BoW that are not in KB--future')
        print('   0 -- Exit')
        result = input('Enter choice: ')
        if result == '1':
            lowerCase_NNP_Check(tagged_BoW)
        elif result == '2':
            nnpNotInKB(tagged_BoW, nnxKB)
        elif result == '3':
            print('Not yet...')
        elif result == '0':
            print('Exiting...')
            break
        else:
            print('Something really wrong since you should not be able to get here')
        result = ''

    print('--- End   rectifyKB.py ---')
