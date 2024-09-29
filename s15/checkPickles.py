#
# pickleChecker.py
#

import pickle
from commonConfig import Sentence


if __name__ == "__main__":

    """
    # starterKB
    #
    starterKB = pickle.load(open('pickleJar/starterKB.p', 'rb'))

    print('len starterKB: ', len(starterKB))
    print('type starterKB: ', type(starterKB))

    for k in starterKB:
        print(k)


    
    # booksRead
    #
    booksRead = pickle.load(open('pickleJar/booksRead.p', 'rb'))

    print('len booksRead: ', len(booksRead))
    print('type booksRead: ', type(booksRead))

    for b in booksRead:
        print(b)

    """
    """
    # taggedCorpora
    #
    taggedCorpora = pickle.load(open('pickleJar/taggedCorpora.p', 'rb'))

    print('len taggedCorpora: ', len(taggedCorpora))
    print('type taggedCorpora: ', type(taggedCorpora))

    bookCnt = 0
    for book in taggedCorpora:
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


    """
    
    # processedCorporaSVO: processedCorporaSVO.p
    # outputCorpora (resolved pronouns: resolvedPronuons.p)
    #
    processedCorporaSVO = pickle.load(open('pickleJar/processedCorporaSVO.p', 'rb'))

    print('len processedCorporaSVO: ', len(processedCorporaSVO))
    print('type processedCorporaSVO: ', type(processedCorporaSVO))

    bookCnt = 0
    for book in processedCorporaSVO:
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

    """
    # read processed book(s)
    #
    processedBook = pickle.load(open('books/A_Dog_On_A_Log.p', 'rb'))

    print('len processedBook: ', len(processedBook))
    print('type processedBook: ', type(processedBook))

    for sent in processedBook:
        print('.....')
        print(type(sent))
        sent.printAll()
    
    """
    """
    b4tagging = pickle.load(open('pickleJar/b4tagging.p', 'rb'))

    print('len b4tagging: ', len(b4tagging))
    print('type b4tagging:' , type(b4tagging))

    for i in b4tagging:
        print(i[0]) # book name
        for j in i[1]:
            print(j)
    
    """
