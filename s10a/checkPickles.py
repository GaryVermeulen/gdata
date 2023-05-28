#
# pickleChecker.py
#

import pickle


def getPickles():

    """
    with open('pickles/starterDictList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded startedDictList.pkl')
    fp.close()
    """
    """
    with open('data/ourCorpus.pkl', 'rb') as fp:
        ourCorpus = pickle.load(fp)
        print('Aunt Bee loaded ourCorpus.pkl')
    fp.close()

    with open('data/newDict.pkl', 'rb') as fp:
        newDict = pickle.load(fp)
        print('Aunt Bee loaded newDict.pkl')
    fp.close()
    """
    
    with open('pickles/newTaggedList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()
    

    """
    with open('pickles/inflections.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded inflections.pkl')
    fp.close()
    """
    
    return ourPickle
    


if __name__ == "__main__":

    print('Pickle checker...')
    
    ourPickle = getPickles()

    print('ourPickle:')
    print(len(ourPickle))
    print(type(ourPickle))

#    print(ourPickle)

    for p in ourPickle:
        if p[0] == 'not' or p[0] == 'fast':
            print(p)

    

#    print('-' * 5)
    
    """
    print('newDict:')
    print(len(newDict))
    print(type(newDict))
    print(newDict.get("eat_1"))
    print(newDict.get("do_1"))
    """
    
    """
    # Temp fix for the hammy problem
    newList = []
    for p in ourPickle:
        #print(p)
        if p[0] == 'hammy':
            print('org found: {} at p[0]: {}'.format(p, p[0]))
            if p[1] != 'NNP':
                newList.append((p[0],'NNP'))
            else:
                newList.appned(p)
        else:
            newList.append(p)
    
    for n in newList:
        if n[0] == 'hammy':
            print('new found: {} at n[0]: {}'.format(n, n[0]))

    # Save modified pickle...
    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(newList, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()
    """

    """
    cnt = 1
    testWord = 'walked'
    print('looking for: ', testWord)
    for p in ourPickle:
        if testWord in p:
            print('found {} at {} {}'.format(testWord, cnt, p))
        cnt += 1
        
    """

    """
    # Checking inflections...
    #print(ourPickle[2000:2020:]) # Just look at some
    testWord = 'saw' # 'run'
    cnt = 1
    for line in ourPickle:
        if testWord in line:
            print('found {} at {} {}'.format(testWord, cnt, line))
            if line[1] == 'v': # incorrect tag 
                print('found v {} at {} {}'.format(testWord, cnt, line))

        cnt += 1
    """

    """    
    # newTaggedList
    print(ourPickle[0:60:]) # Just look at some
    testWord = 'saw' # 'run'
    cnt = 1
    for line in ourPickle:
#        print(line)
#        print(line[0])
#        print(line[1])
        if testWord in line[0]:
            print('found {} at {} {}'.format(testWord, cnt, line))
#            if line[1] == 'v': # correct tag VB, VBD, etc.
#                print('found v {} at {} {}'.format(testWord, cnt, line))

        cnt += 1
    
    """
    
