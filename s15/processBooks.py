# processBooks.py
#


import pickle
from commonConfig import punctuationMarks, nnx
from commonUtils import connectMongo
from scrapeWord import scrapeWord
from resolvePronouns import resolvePronouns
from resolvePronouns import resolvePronounsV2
from tallyBookSubjects import tallyBookSubjects

from collections import Counter


pickleIn = 'pickleJar/processedCorporaSVO.p'


def loadPickleData():

    with open(pickleIn, 'rb') as fp:
        corpora = pickle.load(fp)
    fp.close()

    return corpora



#def reduceFields(bookSents):
#
#    bookSentsReduced = []
#
#    for s in bookSents:
#        print(s.taggedSent)
#        newSent = []
#        for word in s.taggedSent:
#            print(word)
#            newWord = {'word': word['word'], 'pos': word['pos'], 'tag': word['tag']}
#            print(newWord)
#            newSent.append(newWord)
#        print(newSent)
#
#        bookSentsReduced.append(newSent)
#    
#    return bookSentsReduced

    
#def resolvePronouns(bookSents):
#
#    epistropheSents = []
#
#    for s in bookSents:
#        print(s.inputSent)
#        print(s.taggedSent)
#        print('=====================')
#
#
#    return epistropheSents



def search(searchValue, listOfDicts):
    return [element for element in listOfDicts if element['word'] == searchValue]

def searchList(searchValue, workList):
    return [element for element in workList if element[0] == searchValue]


# Come to find out--must resolve pronouns first :-(
def processBookSubjects(inputList):

    global resList

    if len(inputList) <= 0:
        print("NO INPUT")
        return
    else:
        print("INPUT: ", inputList)

    workList = inputList.copy()

    for i in workList:
        print('i: ', i)
        
        searchItem = i[0]
        #tmpList = search(searchItem, workList)
        tmpList = searchList(searchItem, workList)

        tmpListLen = len(tmpList)

        if tmpListLen > 0:
            resList.append((tmpListLen, i))

        for j in tmpList:
            tIndex = workList.index(j)
            popped = workList.pop(tIndex)

        processBookSubjects(workList)
        
    return



#def createBookBOW(bookName, bookSents):
#
#    bow = []
#    tmpWords = []
#    
#    for s in bookSents:
#        #print(bookName)
#        #print(s)
#        #for w in s.inputSent:
#        #    if w not in punctuationMarks:
#        #        print(w.lower())
#        #        if w.lower() not in tmpWords:
#        #            tmpWords.append(w.lower())
#
#        for i in s.taggedSent:
#            #print(i)
#            word = i["word"]
#            tag = i["tag"]
#
#            #print(word, tag)
#
#            if word not in punctuationMarks:
#                if (word.lower(), tag) not in tmpWords:
#                    tmpWords.append((word.lower(), tag))
#                    #print(tmpWords)
#
#        #print('---')
#
#    bow.append((bookName, tmpWords))
#
#    #for b in bow:
#    #    print(b[0])
#    #    print(b[1])
#
#    return bow



#
#
#
if __name__ == "__main__":

    print("Start: processBooks...")
    bookList = []
    unknownWords = []
    knownWords = []
    eBooks = []
    oBooks = []

    resList = []
    
    mdb = connectMongo()
    simpDB = mdb["simp"]
    starterKB = simpDB["starterKB"]
    simpDictionary = simpDB["simpDictionary"]
    webDictionary = simpDB["webDictionary"]
    simpVocabulary = simpDB["simpVocabulary"]
    inflectionsCol = simpDB["inflectionsCol"]

    corpora = loadPickleData()



    # Create a BOWs for each book to determine unknown vocabulary
    # word(s), search dictionaries (and web if not in dictionary),
    # add dictionary word to vocabulary, and then save books
    #
    # Rev 2: Not sure a BOW will buy us what we really need i.e. context and comprehension.
    # So now let's try working on one sentence at a time... Still checking if we know the word
    #
    # Rev 3: Looks like we need to resolve pronouns first :-(
    #

#    inputBooks = []
#    outputBooks = []
    
    for corpus in corpora:
        #print(corpus[0])
        bookName = corpus[0]
        bookSents = corpus[1]
        workList = []
        print(bookName)
        print(bookSents)

#        for s in bookSents:
#            s.printAll()
#            print('..........')

        
        print('..........')

        epistropheSents = resolvePronouns(bookSents)
        
        print('len booksSents     : ', len(bookSents))
        print('len epistropheSents: ', len(epistropheSents))
#
        for s in epistropheSents:
            #print(s.taggedSentShort)
            print(s.epistropheSent)
            #print("---")
            for w in s.taggedSentShort:
                print(w["word"], end =" ")

            print("\n")
            for w in s.epistropheSent:
                print(w[0], end =" ")


            print('\nSubjects:')
            print(s.subject)
                
            #print(s.epistropheSent)
            #workList.append(s.epistropheSent)
            print('\n..........')

#        epistropheSents = resolvePronounsV2(bookSents)
#        print('..........')
#        for s in epistropheSents:
#            print(s)
 
        # Both versions of resolvePronouns need work...
        # Contiuning with what we have:
        #

        #for s in epistropheSents:
        #    s.printAll()

        if bookName == 'JimmysFirstDayOfSchool':
            print('*** Before tally...********************************')
            #tallyBookSubjects(epistropheSents)

            #processBookSubjects(workList)

            #for r in resList:
            #    print('r: ', r)
            
            print('*** After tally...********************************')
        else:
            print('bookName: ', bookName)
        
            
    
        
    print('----------')
    print("\nCompleted: processBooks.")
