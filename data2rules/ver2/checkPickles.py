#
# pickleChecker.py
#

import pickle
#from commonConfig import Sentence


def getPickles():

    with open('pData/processedKB.p', 'rb') as fp: # Has "cartoon" entry
        processedKB = pickle.load(fp)
        print('Aunt Bee loaded processedKB.p')
    fp.close()

    with open('pData/starterKB.p', 'rb') as fp: # No entry for "cartoon"
        starterKB = pickle.load(fp)
        print('Aunt Bee loaded starterKB.p')
    fp.close()

    with open('pData/taggedCorpora.p', 'rb') as fp:
        taggedCorpora = pickle.load(fp)
        print('Aunt Bee loaded taggedCorpora.p')
    fp.close()
    
    return processedKB, starterKB, taggedCorpora



if __name__ == "__main__":


    processedKB, starterKB, taggedCorpora = getPickles()

    print('processedKB:')
    print('len kb: ', len(processedKB))
    print('type kb: ', type(processedKB))

    for item in processedKB:
        print(item)

    print('starterKB:')
    print('len kb: ', len(starterKB))
    print('type kb: ', type(starterKB))

    for item in starterKB:
        print(item)

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
            
