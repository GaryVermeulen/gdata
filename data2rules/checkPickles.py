#
# pickleChecker.py
#

import pickle
#from commonConfig import Sentence


def getPickles():

    with open('data/ourDict.pkl', 'rb') as fp:
        ourDict = pickle.load(fp)
        print('Aunt Bee loaded ourDict.pkl')
    fp.close()

    with open('data/ourCorpus.pkl', 'rb') as fp:
        ourCorpus = pickle.load(fp)
        print('Aunt Bee loaded ourCorpus.pkl')
    fp.close()

    with open('data/newDict.pkl', 'rb') as fp:
        newDict = pickle.load(fp)
        print('Aunt Bee loaded newDict.pkl')
    fp.close()
    
    return ourDict, ourCorpus, newDict



if __name__ == "__main__":

    """

    ourDict, ourCorpus, newDict = getPickles()

    print('ourDict:')
    print(len(ourDict))
    print(type(ourDict))
    print(ourDict.get("pookie_1"))
    print(ourDict.get("jimmy_1"))
    
    for key, value in ourDict.items():
        print(key, value)
        print(ourDict[key]['Word'])
        print(ourDict[key]['Tag'])
    print('-' * 5)
    print('ourCorpus:')
    print(len(ourCorpus))
    print(type(ourCorpus))
    print('-' * 5)
    print('newDict:')
    print(len(newDict))
    print(type(newDict))
    print(newDict.get("pookie_1"))
    print(newDict.get("jimmy_1"))
    


    objArr = pickle.load( open("data/foundSVO.p", "rb" ) )

    print('len objArr: ', len(objArr))
    print('type objArr: ', type(objArr))

    for obj in objArr:
        
        print('bookName: ', obj[0])
        for o in obj[1]:
            o.printAll()
            print('---')
            
        print('--------')
    
    
    untaggedBook = pickle.load(open('data/untaggedCorpora.p', 'rb'))

    print('len untaggedBook: ', len(untaggedBook))
    print('type untaggedBook: ', type(untaggedBook))

    for sent in untaggedBook:
        print('-----')
        print(sent)
        
        
    

    processedCorpora = pickle.load(open('data/processedCorpora.p', 'rb'))

    print('len processedCorpora: ', len(processedCorpora))
    print('type processedCorpora: ', type(processedCorpora))

    bookCnt = 0
    for book in processedCorpora:
        bookCnt += 1
        
        print('-----')
        print('bookCnt: ', bookCnt)
        print(type(book))
        bookName = book[0]
        bookSents = book[1]
        print(book)

        for sent in bookSents:
            print('.....')
            print(type(sent))
            sent.printAll()
            #print(len(sent))
            #print(sent)
            #for word in sent:
            #    print(word, word.tag_, word.dep_)
        
    """

    pickleFile = 'processedKB.p'

    with open(pickleFile, 'rb') as fp:
        kb = pickle.load(fp)
        print('Aunt Bee loaded processedKB.p')
    fp.close()

    print('len kb: ', len(kb))
    print('type kb: ', type(kb))

    for k in kb:
        print(k)

    result = input("add cartoon <y/n>? ")

    if result in ['y', 'Y']:
        kb.insert(8, {'word': 'cartoon', 'tag': 'NN', 'isNonfiction': False, 'isAlive': False, 'CanDo': 'TBD', 'superclass': 'kbroot'})

        print("------")
        for k in kb:
            print(k)

        with open(pickleFile, 'wb') as fp:
            pickle.dump(kb, fp)
        print('Aunt Bee wrote/dumped processedKB.p')
        fp.close()
                  
