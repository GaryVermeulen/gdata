#
# pickleChecker.py
#

import pickle


def getPickles():

    """
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
    """

    with open('newTaggedList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()
    
    return ourPickle



if __name__ == "__main__":

    ourPickle = getPickles()
    """
    print('ourDict:')
    print(len(ourDict))
    print(type(ourDict))
    print(ourDict.get("eat_1"))
    print(ourDict.get("do_1"))
    
    for key, value in ourDict.items():
        print(key, value)
        print(ourDict[key]['Word'])
        print(ourDict[key]['Tag'])
    print('-' * 5)
    print('ourCorpus:')
    print(len(ourCorpus))
    print(type(ourCorpus))
    print('-' * 5)
    """
    """
    print('newDict:')
    print(len(newDict))
    print(type(newDict))
    print(newDict.get("eat_1"))
    print(newDict.get("do_1"))
    """
    print('ourPickle:')
    print(len(ourPickle))
    print(type(ourPickle))

    newList = []
    for p in ourPickle:
        #print(p)
        if p[0] == 'hammy':
            print('found: {} at p[0]: {}'.format(p, p[0]))
            if p[1] != 'NNP':
                newList.append((p[0],'NNP'))
            else:
                newList.appned(p)
        else:
            newList.append(p)
    
    for n in newList:
        if n[0] == 'hammy':
            print('found: {} at n[0]: {}'.format(n, n[0]))

    # Save modified pickle...
    with open('newTaggedList.pkl', 'wb') as fp:
        pickle.dump(newList, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()
