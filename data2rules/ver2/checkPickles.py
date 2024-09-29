#
# pickleChecker.py
#

import pickle
#from commonConfig import Sentence


def getPickles():

    with open('pData/starterKB.p', 'rb') as fp: 
        starterKB = pickle.load(fp)
        print('Aunt Bee loaded starterKB.p')
    fp.close()

    with open('pData/taggedCorpora.p', 'rb') as fp:
        taggedCorpora = pickle.load(fp)
        print('Aunt Bee loaded taggedCorpora.p')
    fp.close()

    with open('pData/resolvedPronouns.p', 'rb') as fp: 
        resolvedPronouns = pickle.load(fp)
        print('Aunt Bee loaded resolvedPronouns.p')
    fp.close()
    
    return starterKB, taggedCorpora, resolvedPronouns



if __name__ == "__main__":


    starterKB, taggedCorpora, resolvedPronouns = getPickles()

    
    print('starterKB:')
    print('len kb: ', len(starterKB))
    print('type kb: ', type(starterKB))

    for item in starterKB:
        print(item)

    print('--------------------------------------------')

    print('taggedCorpora:')
    print('len kb: ', len(taggedCorpora))
    print('type kb: ', type(taggedCorpora))
    
    for corpus in taggedCorpora:
    
        print(corpus[0]) # book name
        print(corpus[1]) # sentence object
        # For sentence objects
        result = input("Display sentences <Y/n>? ")
        if result in ['y', 'Y']: 
            for sentObj in corpus[1]:
                sentObj.printAll()

    print('--------------------------------------------')
    
    print('resolvedPronouns:')
    print('len kb: ', len(resolvedPronouns))
    print('type kb: ', type(resolvedPronouns))

    for corpus in resolvedPronouns:
    
        print(corpus[0]) # book name
        print(corpus[1]) # sentence object
        # For sentence objects
        result = input("Display sentences <Y/n>? ")
        if result in ['y', 'Y']: 
            for sentObj in corpus[1]:
                sentObj.printAll()
