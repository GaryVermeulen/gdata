#
# pickleChecker.py
#

import pickle
from commonConfig import Sentence


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

    """

    objArr = pickle.load( open("data/objArr.p", "rb" ) )

    print('len objArr: ', len(objArr))
    print('type objArr: ', type(objArr))

    for obj in objArr:
        print('-----')
        
        #print('type obj: ', type(obj))
        #print(obj)
        obj.printAll()
    
    
