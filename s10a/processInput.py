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


def checkCorpus(uI):

    uI_List = uI.split()
    print(uI_List)

    wordSents = []
    xMatch = []

    for w in uI_List:
        for sent in corpus:
            if w in sent:
                wordSents.append(sent)
    print('len wordSents: ', len(wordSents))

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


    return wordSents


if __name__ == "__main__":

    corpus = getCorpus()

    print('len corpus: ', len(corpus))
#    for s in corpus:
#        print(s)

    uI = input('Please enter a sentence: ')
    print(uI)

    xyz = checkCorpus(uI)

#    print(xyz)
