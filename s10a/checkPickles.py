#
# pickleChecker.py
#

import pickle
from simpConfig import FANBOYS


def getPickles():
    
    """
    # List of tuples...
    #152
    #<class 'list'>
    #('animal', 'NN')
    #('instrument', 'NN')
    #('simp', 'NNP')
    #
    with open('pickles/starterDictList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded startedDictList.pkl')
    fp.close()
    """

    """
    # List of lists...
    #246
    #<class 'list'>
    #['i', 'will', 'do', 'my', 'homework', 'right', 'now', 'mom']
    #['i', 'said']
    #['oh']
    #['i', 'just', 'could', 'not', 'wait']
    #
    with open('pickles/newCorpus.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newCorpus.pkl')
    fp.close()
    """

    """
    # List of dictionaries...
    #31
    #<class 'list'>
    #{'name': 'sam', 'ppt': 'P', 'tag': 'NNP', 'canDo': 'see,eat,walk,run', 'superclass': 'man'}
    #{'name': 'pookie', 'ppt': 't', 'tag': 'NNP', 'canDo': 'see,eat,walk,run', 'superclass': 'cat'}
    #{'name': 'daffy', 'ppt': 't', 'tag': 'NNP', 'canDo': 'see,eat,walk,run,fly', 'superclass': 'duck'}
    #
    with open('pickles/newKB_Dict.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newKB_Dict.pkl')
    fp.close()
    """
    
    
    # List of tuples from corpus...
    #724
    #<class 'list'>
    #('however', 'RB')
    #('before', 'IN')
    #('i', 'PRP')
    #('can', 'MD')
    #
    with open('pickles/newTaggedList.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()
    

    """
    # List of lists...
    #112505
    #<class 'list'>
    #['acadia', 'n', 'acadias', 'acadiae']
    #['acadian', 'n', 'acadians']
    #['acalepha', 'n', 'acalephae']
    #['acalypha', 'n', 'acalyphas', 'acalyphae']
    #
    with open('pickles/inflections.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded inflections.pkl')
    fp.close()
    """

    """
    653
    <class 'dict'>
    key:  however
    val:  [[['however'], ['RB'], []], [['however'], ['conjunction'], [], [':', 'in', 'whatever', 'manner', 'or', 'way', 'that']], [['however'], ['conjunction'], [], [':', 'although']], [['however'], ['adverb'], [], [':', 'in', 'whatever', 'manner', 'or', 'way']], [['however'], ['adverb'], [], [':', 'to', 'whatever', 'degree', 'or', 'extent']], [['however'], ['adverb'], [], [':', 'in', 'spite', 'of', 'that', ':', 'on', 'the', 'other', 'hand']], [['however'], ['adverb'], [], [':', 'how', 'in', 'the', 'world']]]
    ---
    [['however'], ['RB'], []]
    [['however'], ['conjunction'], [], [':', 'in', 'whatever', 'manner', 'or', 'way', 'that']]
    [['however'], ['conjunction'], [], [':', 'although']]
    [['however'], ['adverb'], [], [':', 'in', 'whatever', 'manner', 'or', 'way']]
    [['however'], ['adverb'], [], [':', 'to', 'whatever', 'degree', 'or', 'extent']]
    [['however'], ['adverb'], [], [':', 'in', 'spite', 'of', 'that', ':', 'on', 'the', 'other', 'hand']]
    [['however'], ['adverb'], [], [':', 'how', 'in', 'the', 'world']]
    ----------
    key:  before
    val:  [[['before'], ['IN'], []], [['before'], ['adverb'], [], [':', 'in', 'advance', ':', 'ahead']], [['before'], ['adverb'], [], [':', 'at', 'an', 'earlier', 'time']], [['before'], ['preposition'], [], [':', 'forward', 'of', ':', 'in', 'front', 'of']], [['before'], ['preposition'], [], [':', 'in', 'the', 'presence', 'of']], [['before'], ['preposition'], [], [':', 'under', 'the', 'jurisdiction', 'or', 'consideration', 'of']], [['before'], ['preposition'], [], [':', 'at', 'the', 'disposal', 'of']], [['before'], ['preposition'], [], [':', 'in', 'store', 'for']], [['before'], ['preposition'], [], [':', 'preceding', 'in', 'time', ':', 'earlier', 'than']], [['before'], ['preposition'], [], [':', 'in', 'a', 'higher', 'or', 'more', 'important', 'position', 'than']], [['before'], ['conjunction'], [], [':', 'earlier', 'than', 'the', 'time', 'that']], [['before'], ['conjunction'], [], [':', 'sooner', 'or', 'quicker', 'than']], [['before'], ['conjunction'], [], [':', 'so', 'that', '…', 'do', 'not']], [['before'], ['conjunction'], [], [':', 'until', 'the', 'time', 'that']], [['before'], ['conjunction'], [], [':', 'or', 'else', '…', 'not']], [['before'], ['conjunction'], [], [':', 'or', 'else']], [['before'], ['conjunction'], [], [':', 'rather', 'or', 'sooner', 'than']]]
    ---
    [['before'], ['IN'], []]
    [['before'], ['adverb'], [], [':', 'in', 'advance', ':', 'ahead']]
    [['before'], ['adverb'], [], [':', 'at', 'an', 'earlier', 'time']]
    [['before'], ['preposition'], [], [':', 'forward', 'of', ':', 'in', 'front', 'of']]
    [['before'], ['preposition'], [], [':', 'in', 'the', 'presence', 'of']]
    [['before'], ['preposition'], [], [':', 'under', 'the', 'jurisdiction', 'or', 'consideration', 'of']]
    [['before'], ['preposition'], [], [':', 'at', 'the', 'disposal', 'of']]
    [['before'], ['preposition'], [], [':', 'in', 'store', 'for']]
    [['before'], ['preposition'], [], [':', 'preceding', 'in', 'time', ':', 'earlier', 'than']]
    [['before'], ['preposition'], [], [':', 'in', 'a', 'higher', 'or', 'more', 'important', 'position', 'than']]
    [['before'], ['conjunction'], [], [':', 'earlier', 'than', 'the', 'time', 'that']]
    [['before'], ['conjunction'], [], [':', 'sooner', 'or', 'quicker', 'than']]
    [['before'], ['conjunction'], [], [':', 'so', 'that', '…', 'do', 'not']]
    [['before'], ['conjunction'], [], [':', 'until', 'the', 'time', 'that']]
    [['before'], ['conjunction'], [], [':', 'or', 'else', '…', 'not']]
    [['before'], ['conjunction'], [], [':', 'or', 'else']]
    [['before'], ['conjunction'], [], [':', 'rather', 'or', 'sooner', 'than']]
    """
    """
    with open('pickles/mainDictionary.pkl', 'rb') as fp:
        ourPickle = pickle.load(fp)
        print('Aunt Bee loaded mainDictionary.pkl')
    fp.close()
    """
    
    return ourPickle
    

def fixPickle(ourPickle):

    betterPickle = []

    print('Before fix: ', len(ourPickle))

    # Correct CC to only FANBOYS
    for p in ourPickle:
        if p[1] == 'CC':
            if p[0] in FANBOYS:
                tmpToken = (p[0], p[1])
                betterPickle.append(tmpToken)
        else:
            betterPickle.append(p)
                
    print('After fix: ', len(betterPickle))

    return betterPickle


def savePickle(p):

    with open('pickles/newTaggedList.pkl', 'wb') as fp:
        pickle.dump(p, fp)
        print('Aunt Bee made a newTaggedList pickle')
    fp.close()
    


if __name__ == "__main__":

    limit = 1

    print('Pickle checker...')
    
    ourPickle = getPickles()

    print('ourPickle:')
    print(len(ourPickle))
    print(type(ourPickle))

#    print(ourPickle)

    """
    # list the 1st 100 entries
    for p in ourPickle:
        if limit > 100:
            break
        print(p)
        limit += 1
    """

    # Checking for a word
    for p in ourPickle:
        
        if p[0] == 'hammy':
            print(p)
        
        """
        if 'hammy' in p:
            print(p)
        """
    """
    for w, d in ourPickle.items():
        if limit > 100:
            break
        print('key: ', w)
        print('val: ',d)
        print('---')
        for v in d:
            print(v)
        print('-' * 10)
        limit += 1
    """
    """
    print(len(ourPickle))
    print(type(ourPickle))
    """
        
    """
        if p[0] == 'not' or p[0] == 'fast':
            print('not | fast: ', p)
        if p[1] == 'CC':
            print('CC: ', p)
            
    bP = fixPickle(ourPickle)

    for p in bP:
        if p[0] == 'not' or p[0] == 'fast':
            print('not | fast: ', p)
        if p[1] == 'CC':
            print('CC: ', p)
    """
#    savePickle(bP)

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
    testWord = 'pookie'
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
    
