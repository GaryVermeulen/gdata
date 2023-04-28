#
# processInput.py
#

import pickle

def getCorpus():

    with open('newCorpus.pkl', 'rb') as fp:
        corpus = pickle.load(fp)
        print('Aunt Bee loaded newCorpus.pkl')
    fp.close()

    return corpus


def getNewTaggedList():

    with open('newTaggedList.pkl', 'rb') as fp:
        newTaggedList = pickle.load(fp)
        print('Aunt Bee loaded newTaggedList.pkl')
    fp.close()

    return newTaggedList


def isNNx(w):

    for t in newTaggedList:
#        print('t:::: ', t)
#        print(t[0], t[1])
        if w == t[0]:
            if t[1] in ['NN', 'NNP', 'NNS']:
                print('found {} at {}'.format(w, t))
                return True

    return False


def isVBx(w):

    for t in newTaggedList:
#        print('t:::: ', t)
#        print(t[0], t[1])
        if w == t[0]:
            if t[1] in ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']:
                print('found {} at {}'.format(w, t))
                return True

    return False


def checkCorpus(uI):

    print('Processing checkCorpus...')

    uI_List = uI.split()
    print('uI: ', uI_List)

    wordSents = []
    xMatch = []
    wordFound = []

    # Look for input sentence nouns in the corpus
    for sent in corpus:
        for w in uI_List:
            
            print(w)
            print(type(w))
            print(sent)
            t = []
            if w in sent:
                if isNNx(w):
                    t.append(w)
                    t.append(sent)
                    wordFound.append(t)

                
    print('len wordFound: ', len(wordFound))
    print('len wordFound: ', len(wordFound))

    # Of the above what are the verbs?
    for s in wordFound:
        for s_1 in s:
            for x in s_1:
                if isVBx(x):
                    print('found x: {} at: {} and isVBx {}'.format(x, s_1, isVBx(x)))

        
        


    

    """
    for w in uI_List:
        print('w: ', w)
        tmp_wordSent = []
#        tmp_wordSent.append(w)
        for sent in corpus:
            if w in sent and isNNx(w): # Only capture nouns
                tSent = []
                print('found w: {} at: {} and isNNx {}'.format(w, sent, isNNx(w)))
                tSent.append(w)
                tSent.append(sent)
                tmp_wordSent.append(tSent)
                wordSents.append(tmp_wordSent)
        
#    print('len corpus: ', len(corpus))
    print('len wordSents: ', len(wordSents))

    for s in wordSents:
        print(s)

    """

    """

    for s in wordSents: # works when uI is shorter then s
        s_str = ' '.join(s)
        print(s_str)
        res = s_str.find(uI)
        if res > -1:
            xMatch.append(s_str)
    print('xMatch: ', xMatch)

    if len(xMatch) == 0:
        for s in wordSents:
            sSet = set(s)
            uISet = set(uI_List)
            print('sSet: ', sSet)
            print('uISet: ', uISet)
            intersection = sSet.intersection(uISet)
            if len(intersection) > 0:
                xMatch.append(' '.join(s))
            
            
    print('intersection: ', intersection)
        

    if len(xMatch) > 0:

        windowStart = 0
        windowStop = len(uI_List)
        windowStep = 1
        windowCount = 0
        windowSize = len(uI_List)

        print('len uI_List: ', len(uI_List))
        print(uI_List)
        print('len xMatch: ', len(xMatch))
        print(xMatch)
        print('-' * 5)
                                        # Input sentence is longer than matched sentence
        if len(uI_List) <= len(xMatch): # All words in uI_List are in xMatch
            tmpList = xMatch[0].split()
        
            window = tmpList[windowStart:windowStop:windowStep]

            print('tmpList: ', tmpList)
            print('window: ', window)

        
            if len(uI_List) == len(window) and len(uI_List) == sum([1 for i, j in zip(uI_List, window) if i == j]):
                print("The lists are identical")
                print(uI_List)
                print('=')
                print(window)
            else:
                # Move window and try again
                print('moving on...')
                windowStart += 1
                windowStop += 1
                windowCount += 1
                searchedLen = windowCount + windowSize
            
                while searchedLen <= len(tmpList):
                    window = tmpList[windowStart:windowStop:windowStep]
                    if len(uI_List) == len(window) and len(uI_List) == sum([1 for i, j in zip(uI_List, window) if i == j]):
                        print("The lists are identical")
                        print(uI_List)
                        print('=')
                        print(window)
                        break
                    else:
                        print("The lists are not identical")
                        print(uI_List)
                        print('!=')
                        print(window)
                        print('moving on again...')
                        windowStart += 1
                        windowStop += 1
                        windowCount += 1
                        searchedLen = windowCount + windowSize
                        
        elif len(uI_List) >= len(xMatch):   # Input sentence is longer than matched sentence
            print('input sentence longer then xMatch[0]')
            print(uI_list)
            print(xMatch[0])

    """

    return wordSents


if __name__ == "__main__":

    print('Processing processInput...')

    corpus = getCorpus()
    newTaggedList = getNewTaggedList()

    print('len corpus: ', len(corpus))
    print('type corpus: ', type(corpus))
#    for s in corpus:
#        print(s)
    print('-' * 5)
    print('len newTaggedList: ', len(newTaggedList))
    print('type newTaggedList: ', type(newTaggedList))
#    for t in newTaggedList:
#        print(t)
    print('-' * 5)
    
    uI = input('Please enter a sentence: ')
    print(uI)

    print('-' * 5)
    
    xyz = checkCorpus(uI)

    print('-' * 5)
    print('len xyz: ', len(xyz))
    print('type xyz: ', type(xyz))
    for x in xyz:
        print('len x: ', len(x))
        print('type x: ', type(x))
        print(x[0])
        for y in x:
            print('   len y: ', len(y))
            print('   type y: ', type(y))
            print('   ', y)

#    print(xyz)
