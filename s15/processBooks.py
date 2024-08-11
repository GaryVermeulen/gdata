# processSVOs.py
#
# Supplement to Space; Find missing SVOs, and
# check for consistency.


import pickle
from commonConfig import punctuationMarks, nnx
from commonUtils import connectMongo
from scrapeWord import scrapeWord

from collections import Counter


pickleIn = 'pickleJar/processedCorporaSVO.p'


def loadPickleData():

    with open(pickleIn, 'rb') as fp:
        corpora = pickle.load(fp)
    fp.close()

    return corpora


def createBookBOW(bookName, bookSents):

    bow = []
    tmpWords = []
    
    for s in bookSents:
        #print(bookName)
        #print(s)
        #for w in s.inputSent:
        #    if w not in punctuationMarks:
        #        print(w.lower())
        #        if w.lower() not in tmpWords:
        #            tmpWords.append(w.lower())

        for i in s.taggedSent:
            #print(i)
            word = i["word"]
            tag = i["tag"]

            #print(word, tag)

            if word not in punctuationMarks:
                if (word.lower(), tag) not in tmpWords:
                    tmpWords.append((word.lower(), tag))
                    #print(tmpWords)

               
        #print('---')

    bow.append((bookName, tmpWords))

    #for b in bow:
    #    print(b[0])
    #    print(b[1])

    return bow



#
#
#
if __name__ == "__main__":

    print("Start: processBooks...")
    bookList = []
    unknownWords = []
    knownWords = []

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

    books = []
    
    for corpus in corpora:
        #print(corpus[0])
        bookName = corpus[0]
        bookList.append(bookName)

        bookSub = []
        

        # sub = {"subject": word, "tag": tag, "count": +=1}

        print('bookName:')
        print(bookName)

        # Reduce dictionay to two keys
        
        for ss in corpus[1]:
            for s in ss.taggedSent:
                print(s)
            print('type: ', ss.type)
            print('subjects: ', ss.subject)
            reducedSS = []
            for sub in ss.subject:
                print('sub: ', sub)

                
                reducedSub = {"word": sub["word"], "tag": sub["tag"]}
                reducedSS.append(reducedSub)

            for rs in reducedSS:
                print('rs: ', rs)
        
                bookSub.append(rs)

        books.append((bookName, bookSub))

    print('..........')

    for b in books:

        counter = Counter(b[1])


        duplicates = list(filter(lambda x: x[1]>1, counter.items()))
        if duplicates:
            for item in duplicates:
                print(f'{item[0]} - {item[1]}')
        else:
            print('No duplicates')

        print('---')
    #my_dict = {i:MyList.count(i) for i in MyList}

#    for b in books:
#        print('b[0]: ', b[0])
#        
#        subCntDict = {i:b.count(i) for i in b}
#
#        print(subCntDict)



    """
    cleanBooks = []
    for bs in books:
        bn = bs[0]
        tmpS = []
        print('bs[0]: ', bs[0])
        cnt = 0
        for b in bs[1]:
            cnt += 1
            print('cnt b: ', cnt, b)
            if b not in tmpS:
                tmpS.append(b)
        cleanBooks.append((bn, tmpS))

    print('..........')

    
    for cb in cleanBooks:
        print('cb[0]: ', cb[0])
        cnt = 0
        for c in cb[1]:
            cnt += 1
            print('cnt c: ', cnt, c)

    """

#                if sub not in bookSubjects:
#                    bookSubjects.append(sub)
#                    print("*** ADD: ", sub)
#                else:
#                    print("*** IN: ", sub)
                    
            #print('verb: ', ss.verb)
            #print('object: ', ss.object)
#            print()

#        books.append((bookName, bookSubjects))

#        print('-----')

#    print("==========")
#    for x in books:
#        print(x[0])
#        for y in x[1]:
#            print(y)

    """
        bookBOW = createBookBOW(corpus[0], corpus[1])

        print('-----')
        
        for i in bookBOW:
            print(i[0])
            print(i[1])
        
            for w in i[1]:
                print('w: ', w)
                wCap = w[0].capitalize()
                tag = w[1]
                print(wCap, tag)
                query = {"word": wCap}

                if tag in nnx:
                    # starterKB words are mixed case i.e. NNPs are upper case while NNs are lower
                    if tag in ['NN', 'NNS']: # Search for lower case
                        query = {"word": w[0]}

                    doc = list(starterKB.find(query))
                    if len(doc) > 0:
                        #for d in doc:
                        #    print('d: ')
                        #    print(d)
                        print('{} found in starterKB using: {}'.format(w, query))
                        knownWords.append(w)
                    else:
                        print('{} not found in starterKB using: {}'.format(w, query))
                        unknownWords.append(w)

                else:         
                    doc = list(simpVocabulary.find(query))
                    if len(doc) > 0:
                        #for d in doc:
                        #    print('d: ')
                        #    print(d)
                        print('{} found in simpVocabulary using: {}'.format(w, query))
                        knownWords.append(w)
                    else:
                        print('{} not in simpVocabulary using: {}, searching simpDictionary'.format(w, query))
                        dictDoc = list(simpDictionary.find(query))
                        if len(dictDoc) > 0:
                            #for d in dictDoc:
                            #    print('d: ')
                            #    print(d)
                            #    x = simpVocabulary.insert_one(d)
                            #    print('x: ', x)
                            print('{} found in simpDictionary using: {}'.format(w, query))
                            knownWords.append(w)
                        else:
                            print('{} not in simpDictionary using: {}, searching webDictionary'.format(w, query))
                            webDictDoc = list(simpDictionary.find(query))
                            if len(webDictDoc) > 0:
                                #for d in webDictDoc:
                                #    print('d: ')
                                #    print(d)
                                #    x = simpVocabulary.insert_one(d)
                                #    print('x: ', x)
                                print('{} found in webDictionary using: {}'.format(w, query))
                                knownWords.append(w)
                            else:
                                print('{} not in webDictionary using: {}, searching web (scrapeWord)'.format(w, query))
                                results = scrapeWord(w)
                                if results == None:
                                    print('scrapeWord retunred: None for:', w)
                                    unknownWords.append(w)
                                else:
                                    print('scrapeWord retunred: {} for: {}'.format(len(results), w))
                                    
                                    #print('results:')
                                    #for r in results:
                                    #    print(r)
                                    #    webDictionary.insert_one(r)
                                    #    x = simpVocabulary.insert_one(r)
                                    #    print('x: ', x)
                                    knownWords.append(w)
                        
                        ###unknownWords.append(w)

        print('-----')
        for u in unknownWords:
            print('unknown: ', u)

        for k in knownWords:
            print('known: ', k)
            
                
    """    
    """
        print('-----')
        # Inflections just do not have what we need...
        #
        print("Searching inflectionsCol:")
        for u in unknownWords:
            print('u: ', u)
            query = {"word": u}
            doc = list(inflectionsCol.find(query))
            if len(doc) > 0:
                for d in doc:
                    print('d: ')
                    print(d)
            else:
                print('Not in inflectionsCol')

        print('-----')
        # Save book
        with open('books/' + bookName + '.p', "wb") as f:
            pickle.dump(corpus[1], f)
    """    

    print("Completed: processBooks.")
