# processSVOs.py
#
# Supplement to Space; Find missing SVOs, and
# check for consistency.


import pickle
from commonConfig import punctuationMarks
from commonUtils import connectMongo


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
        print(bookName)
        print(s)
        for w in s.inputSent:
            
            if w not in punctuationMarks:
                print(w.lower())
                if w.lower() not in tmpWords:
                    tmpWords.append(w.lower())
                
        print('---')

    bow.append((bookName, tmpWords))

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
    simpDictionary = simpDB["simpDictionary"]
    simpVocabulary = simpDB["simpVocabulary"]
    inflectionsCol = simpDB["inflectionsCol"]

    corpora = loadPickleData()



    # Create BOW to determine unknown vocabulary word(s), search dictionary,
    # add dictionary word to vocabulary, and then save books
    for corpus in corpora:
        print(corpus[0])
        bookName = corpus[0]
        bookList.append(bookName)


        bookBOW = createBookBOW(corpus[0], corpus[1])

        print('-----')

        for i in bookBOW:
            print(i[0])
            print(i[1])

            for w in i[1]:
                print(w)
                wCap = w.capitalize()
                print(wCap)

                query = {"word": wCap}
                doc = list(simpVocabulary.find(query))
                if len(doc) > 0:
                    for d in doc:
                        print('d: ')
                        print(d)
                else:
                    print('Not in vocab, searching dictionary')
                    dictDoc = list(simpDictionary.find(query))
                    if len(dictDoc) > 0:
                        for d in dictDoc:
                            print('d: ')
                            print(d)
                            x = simpVocabulary.insert_one(d)
                            print('x: ', x)
                    else:
                        print('Not in dictionary')
                        unknownWords.append(w)
                        
                
            

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
    

    print("Completed: processBooks.")
