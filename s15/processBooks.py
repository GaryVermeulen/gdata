# processSVOs.py
#
# Supplement to Space; Find missing SVOs, and
# check for consistency.


import pickle
from commonConfig import punctuationMarks, nnx
from commonUtils import connectMongo
from scrapeWord import scrapeWord


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
    for corpus in corpora:
        #print(corpus[0])
        bookName = corpus[0]
        bookList.append(bookName)


        bookBOW = createBookBOW(corpus[0], corpus[1])

        print('-----')
        
        for i in bookBOW:
            print(i[0])
            print(i[1])
        
            for w in i[1]:
                print(w)
                wCap = w[0].capitalize()
                tag = w[1]
                print(wCap, tag)
                query = {"word": wCap}

                if tag in nnx:
                    doc = list(starterKB.find(query))
                    if len(doc) > 0:
                        for d in doc:
                            print('d: ')
                            print(d)
                    else:
                        print('nnx not in starterKB: ', w)
                        unknownWords.append(w)

                else:         
                    doc = list(simpVocabulary.find(query))
                    if len(doc) > 0:
                        for d in doc:
                            print('d: ')
                            print(d)
                    else:
                        print('Not in simpVocabulary, searching simpDictionary')
                        dictDoc = list(simpDictionary.find(query))
                        if len(dictDoc) > 0:
                            for d in dictDoc:
                                print('d: ')
                                print(d)
                                x = simpVocabulary.insert_one(d)
                                print('x: ', x)
                        else:
                            print('Not in simpDictionary, searching webDictionary')
                            webDictDoc = list(simpDictionary.find(query))
                            if len(webDictDoc) > 0:
                                for d in webDictDoc:
                                    print('d: ')
                                    print(d)
                                    x = simpVocabulary.insert_one(d)
                                    print('x: ', x)
                            else:
                                print('Not in webDictionary, searching web (scrapeWord)')
                                results = scrapeWord(w)
                                if results == None:
                                    print('scrapeWord retunred: None: ', w)
                                    unknownWords.append(w)
                                else:
                                    print('results:')
                                    for r in results:
                                        print(r)
                                        webDictionary.insert_one(r)
                                        x = simpVocabulary.insert_one(r)
                                        print('x: ', x)
                        
                        ###unknownWords.append(w)

        print('-----')
        for u in unknownWords:
            print('unknown: ', u)
                
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
